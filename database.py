# database.py
import psycopg2
import pandas as pd
import streamlit as st
import json
from datetime import datetime, timedelta

class DatabaseManager:
    """
    Manages all database operations for the Commercial Manager Assistant application.
    """
    def __init__(self):
        """Initializes the connection to the PostgreSQL database."""
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="portfolio_db",
                user="abdulkerimhasturk", # Your macOS username
                password=""
            )
        except psycopg2.OperationalError as e:
            st.error(f"🔴 DB Connection Error: {e}. Is PostgreSQL running?")
            st.stop()

    def execute_query(self, query, params=None, fetch=None):
        """A generic method to execute database queries safely with manual commits."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                if fetch == 'one':
                    return cursor.fetchone()
                if fetch == 'all':
                    return cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            # Do not show duplicate errors if it's about tables not existing during setup
            if "relation" not in str(e) and "does not exist" not in str(e):
                 st.error(f"DB Query Error: {e}")
            return None

    def initialize_database(self):
        """Creates all tables and inserts sample data if the database is empty."""
        check_table_query = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = 'companies');"
        cursor = self.connection.cursor()
        cursor.execute(check_table_query)
        table_exists = cursor.fetchone()[0]
        cursor.close()
        
        if not table_exists:
            self.create_all_tables()
            self.insert_sample_data()

    def create_all_tables(self):
        """Creates a comprehensive, unified schema to support all four project modules."""
        queries = [
            "DROP TABLE IF EXISTS contract_key_terms, rfx_requirements, partner_performance, contracts, partners, rfx_documents, companies, tco_analyses, kpi_summary CASCADE;",
            """CREATE TABLE companies (company_id SERIAL PRIMARY KEY, company_name VARCHAR(255) NOT NULL UNIQUE, type VARCHAR(50));""",
            """CREATE TABLE contracts (contract_id SERIAL PRIMARY KEY, company_id INTEGER REFERENCES companies(company_id), contract_title VARCHAR(255) NOT NULL, contract_type VARCHAR(50), status VARCHAR(50), expiration_date DATE, risk_score_display VARCHAR(50));""",
            """CREATE TABLE contract_key_terms (term_id SERIAL PRIMARY KEY, contract_id INTEGER REFERENCES contracts(contract_id), term_name VARCHAR(100), term_value TEXT);""",
            """CREATE TABLE tco_analyses (tco_id SERIAL PRIMARY KEY, analysis_name VARCHAR(255), company_id INTEGER REFERENCES companies(company_id), total_cost_5_year NUMERIC(15, 2));""",
            """CREATE TABLE partners (partner_id SERIAL PRIMARY KEY, company_id INTEGER REFERENCES companies(company_id));""",
            """CREATE TABLE partner_performance (perf_id SERIAL PRIMARY KEY, partner_id INTEGER REFERENCES partners(partner_id), kpi_name VARCHAR(100), kpi_value VARCHAR(100), target_value VARCHAR(100));""",
            """CREATE TABLE rfx_documents (rfx_id SERIAL PRIMARY KEY, rfx_title VARCHAR(255), company_id INTEGER REFERENCES companies(company_id), status VARCHAR(50));""",
            """CREATE TABLE rfx_requirements (req_id SERIAL PRIMARY KEY, rfx_id INTEGER REFERENCES rfx_documents(rfx_id), requirement_text TEXT, risk_level VARCHAR(50));""",
            
            # --- THIS IS THE MISSING TABLE THAT CAUSED THE ERROR ---
            """CREATE TABLE kpi_summary (id SERIAL PRIMARY KEY, kpi_name VARCHAR(100) UNIQUE NOT NULL, kpi_value NUMERIC(10, 2), kpi_change NUMERIC(10, 2));"""
        ]
        for query in queries:
            self.execute_query(query)

    def insert_sample_data(self):
        """Populates the database with sample data."""
        self.execute_query("INSERT INTO companies (company_name, type) VALUES ('InnovateTel GmbH', 'Partner'), ('FutureNet Mobile', 'Client'), ('Global Telco Inc.', 'Prospect');")
        today = datetime.now().date()
        self.execute_query("INSERT INTO contracts (company_id, contract_title, contract_type, status, expiration_date, risk_score_display) VALUES (1, 'Reseller - InnovateTel', 'Reseller Agreement', 'Active', %s, 'Medium');", (today + timedelta(days=250),))
        self.execute_query("INSERT INTO contracts (company_id, contract_title, contract_type, status, expiration_date, risk_score_display) VALUES (2, 'MSA - FutureNet', 'Service Agreement (MSA)', 'Active', %s, 'High');", (today + timedelta(days=80),))
        self.execute_query("INSERT INTO partners (company_id) VALUES (1);")
        self.execute_query("INSERT INTO rfx_documents (rfx_title, company_id, status) VALUES ('FutureNet VoNR RFP', 2, 'In Progress');")
        
        # Insert sample KPIs for the dashboard
        self.execute_query("INSERT INTO kpi_summary (kpi_name, kpi_value, kpi_change) VALUES ('win_rate', 72.5, 5.2), ('avg_margin', 28.3, -1.5);")

    def save_contract_and_analysis(self, title, contract_type, analysis_result):
        """Saves a new contract and its extracted key terms to the database."""
        company_name = title.split(" with ")[-1].replace("'", "''") if " with " in title else "Unknown Company"
        company_id_result = self.execute_query("SELECT company_id FROM companies WHERE company_name = %s", (company_name,), fetch='one')
        if company_id_result:
            company_id = company_id_result[0]
        else:
            company_id = self.execute_query("INSERT INTO companies (company_name, type) VALUES (%s, 'Client') RETURNING company_id;", (company_name,), fetch='one')[0]

        risk_score = "Low"
        if analysis_result and 'risk_analysis' in analysis_result:
            risks = [risk.get('risk_level', 'Low') for risk in analysis_result['risk_analysis']]
            if "High" in risks: risk_score = "High"
            elif "Medium" in risks: risk_score = "Medium"

        contract_id = self.execute_query(
            "INSERT INTO contracts (company_id, contract_title, contract_type, status, risk_score_display) VALUES (%s, %s, %s, 'Active', %s) RETURNING contract_id;",
            (company_id, title, contract_type, risk_score), fetch='one'
        )[0]

        key_terms = analysis_result.get('key_terms', {})
        for term, value in key_terms.items():
            self.execute_query(
                "INSERT INTO contract_key_terms (contract_id, term_name, term_value) VALUES (%s, %s, %s);",
                (contract_id, term, str(value))
            )
        return contract_id

    def get_contracts(self):
        query = "SELECT c.contract_id, c.contract_title, co.company_name AS counterparty, c.contract_type, c.status, c.expiration_date, c.risk_score_display FROM contracts c JOIN companies co ON c.company_id = co.company_id ORDER BY c.contract_id DESC;"
        results = self.execute_query(query, fetch='all')
        if not results: return pd.DataFrame()
        return pd.DataFrame(results, columns=['ID', 'Contract Title', 'Counterparty', 'Type', 'Status', 'Expiry Date', 'Risk Score'])

    def get_expiring_contracts(self, days=90):
        query = "SELECT contract_title, expiration_date FROM contracts WHERE expiration_date BETWEEN NOW() AND NOW() + INTERVAL '%s days' ORDER BY expiration_date ASC;"
        results = self.execute_query(query, (days,), fetch='all')
        if not results: return pd.DataFrame()
        return pd.DataFrame(results, columns=['contract_title', 'expiration_date'])
        
    def get_kpi_summary(self):
        """Fetches dashboard KPIs and returns a correctly structured dictionary even on failure."""
        results = self.execute_query("SELECT kpi_name, kpi_value, kpi_change FROM kpi_summary;", fetch='all')
        # --- THIS IS THE SECOND FIX ---
        # We now return a properly structured dictionary if the query fails, preventing the TypeError
        if not results:
            return {
                'win_rate': {'value': 0, 'change': 0},
                'avg_margin': {'value': 0, 'change': 0}
            }
        return {row[0]: {'value': row[1], 'change': row[2]} for row in results}

    def get_partner_performance(self, partner_company_id):
        query = "SELECT pp.kpi_name, pp.kpi_value, pp.target_value FROM partner_performance pp JOIN partners p ON pp.partner_id = p.partner_id WHERE p.company_id = %s;"
        results = self.execute_query(query, (partner_company_id,), fetch='all')
        if not results: return pd.DataFrame()
        return pd.DataFrame(results, columns=['KPI', 'Actual Value', 'Target'])

    def get_rfx_requirements(self, rfx_id):
        query = "SELECT requirement_text, risk_level FROM rfx_requirements WHERE rfx_id = %s;"
        results = self.execute_query(query, (rfx_id,), fetch='all')
        if not results: return pd.DataFrame()
        return pd.DataFrame(results, columns=['Requirement', 'Assessed Risk Level'])
