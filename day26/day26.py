#Day26
import streamlit as st

# Connect to Snowflake
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

st.title(":material/smart_toy: Introduction to Cortex Agents")
st.write("Learn how to create Cortex Agents with Cortex Search on sales conversations.")

st.session_state.setdefault("agent_created", False)

# Sidebar config
with st.sidebar:
    st.header(":material/settings: Configuration")
    db_name = "CHANINN_SALES_INTELLIGENCE"
    schema_name = "DATA"
    agent_name = "SALES_CONVERSATION_AGENT"
    search_service = "SALES_CONVERSATION_SEARCH"
    
    st.text_input("Database:", db_name, disabled=True)
    st.text_input("Schema:", schema_name, disabled=True)
    st.text_input("Agent Name:", agent_name, disabled=True)
    st.text_input("Search Service:", search_service, disabled=True)
    st.caption("These values match the agent configuration in Day 27")
    st.divider()
    
    if st.button(":material/refresh: Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# Tabs
tab0, tab1 = st.tabs([":material/database: Data Setup", ":material/build: Create Agent"])

# Data Setup Tab
with tab0:
    # Step 1: Database & Schema
    st.markdown("---\n### Step 1: Create Database & Schema")
    setup_step1 = f"""-- Create database and schema (for Days 26-28)
    CREATE OR REPLACE DATABASE "{db_name}";
    CREATE OR REPLACE SCHEMA "{db_name}"."{schema_name}";
    -- Note: USE statements not needed in Streamlit in Snowflake
    -- All subsequent queries will use fully qualified names"""
    st.code(setup_step1, language="sql")
    
    if st.button(":material/play_arrow: Run Step 1", key="run_step1", use_container_width=True):
        with st.spinner("Creating database and schema..."):
            try:
                # Create database and schema (no USE statements in SiS)
                session.sql(f'CREATE OR REPLACE DATABASE "{db_name}"').collect()
                session.sql(f'CREATE OR REPLACE SCHEMA "{db_name}"."{schema_name}"').collect()
                st.success("✓ Step 1 complete!")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Step 2: Sales Conversations
    st.markdown("---\n### Step 2: Create Sales Conversations Table")
    setup_step2 = f"""-- Create table for conversation transcripts
CREATE OR REPLACE TABLE "{db_name}"."{schema_name}".SALES_CONVERSATIONS (
    conversation_id VARCHAR, 
    transcript_text TEXT, 
    customer_name VARCHAR, 
    deal_stage VARCHAR,
    sales_rep VARCHAR, 
    conversation_date TIMESTAMP, 
    deal_value FLOAT, 
    product_line VARCHAR
);
-- Insert 10 comprehensive conversation transcripts"""
    st.code(setup_step2, language="sql")
    
    if st.button(":material/play_arrow: Run Step 2", key="run_step2", use_container_width=True):
        with st.spinner("Creating table and inserting data..."):
            try:
                session.sql(f"""CREATE OR REPLACE TABLE "{db_name}"."{schema_name}".SALES_CONVERSATIONS (
                    conversation_id VARCHAR, transcript_text TEXT, customer_name VARCHAR, deal_stage VARCHAR,
                    sales_rep VARCHAR, conversation_date TIMESTAMP, deal_value FLOAT, product_line VARCHAR)""").collect()
                
                session.sql(f"""INSERT INTO "{db_name}"."{schema_name}".SALES_CONVERSATIONS 
                (conversation_id, transcript_text, customer_name, deal_stage, sales_rep, conversation_date, deal_value, product_line) VALUES
                ('CONV001', 'Initial discovery call with TechCorp Inc''s IT Director and Solutions Architect. Client showed strong interest in our enterprise solution features, particularly the automated workflow capabilities. Main discussion centered around integration timeline and complexity. They currently use Legacy System X for their core operations and expressed concerns about potential disruption during migration. Team asked detailed questions about API compatibility and data migration tools. Action items: 1) Provide detailed integration timeline document 2) Schedule technical deep-dive with their infrastructure team 3) Share case studies of similar Legacy System X migrations. Client mentioned Q2 budget allocation for digital transformation initiatives. Overall positive engagement with clear next steps.', 'TechCorp Inc', 'Discovery', 'Sarah Johnson', '2024-01-15 10:30:00', 75000, 'Enterprise Suite'),
                ('CONV002', 'Follow-up call with SmallBiz Solutions'' Operations Manager and Finance Director. Primary focus was on pricing structure and ROI timeline. They compared our Basic Package pricing with Competitor Y''s small business offering. Key discussion points included: monthly vs. annual billing options, user license limitations, and potential cost savings from process automation. Client requested detailed ROI analysis focusing on: 1) Time saved in daily operations 2) Resource allocation improvements 3) Projected efficiency gains. Budget constraints were clearly communicated - they have a maximum budget of $30K for this year. Showed interest in starting with basic package with room for potential upgrade in Q4. Need to provide competitive analysis and customized ROI calculator by next week.', 'SmallBiz Solutions', 'Negotiation', 'Mike Chen', '2024-01-16 14:45:00', 25000, 'Basic Package'),
                ('CONV003', 'Strategy session with SecureBank Ltd''s CISO and Security Operations team. Extremely positive 90-minute deep dive into our Premium Security package. Customer emphasized immediate need for implementation due to recent industry compliance updates. Our advanced security features, especially multi-factor authentication and encryption protocols, were identified as perfect fits for their requirements. Technical team was particularly impressed with our zero-trust architecture approach and real-time threat monitoring capabilities. They''ve already secured budget approval and have executive buy-in. Compliance documentation is ready for review. Action items include: finalizing implementation timeline, scheduling security audit, and preparing necessary documentation for their risk assessment team. Client ready to move forward with contract discussions.', 'SecureBank Ltd', 'Closing', 'Rachel Torres', '2024-01-17 11:20:00', 150000, 'Premium Security'),
                ('CONV004', 'Comprehensive discovery call with GrowthStart Up''s CTO and Department Heads. Team of 500+ employees across 3 continents discussed current challenges with their existing solution. Major pain points identified: system crashes during peak usage, limited cross-department reporting capabilities, and poor scalability for remote teams. Deep dive into their current workflow revealed bottlenecks in data sharing and collaboration. Technical requirements gathered for each department. Platform demo focused on scalability features and global team management capabilities. Client particularly interested in our API ecosystem and custom reporting engine. Next steps: schedule department-specific workflow analysis and prepare detailed platform migration plan.', 'GrowthStart Up', 'Discovery', 'Sarah Johnson', '2024-01-18 09:15:00', 100000, 'Enterprise Suite'),
                ('CONV005', 'In-depth demo session with DataDriven Co''s Analytics team and Business Intelligence managers. Showcase focused on advanced analytics capabilities, custom dashboard creation, and real-time data processing features. Team was particularly impressed with our machine learning integration and predictive analytics models. Competitor comparison requested specifically against Market Leader Z and Innovative Start-up X. Price point falls within their allocated budget range, but team expressed interest in multi-year commitment with corresponding discount structure. Technical questions centered around data warehouse integration and custom visualization capabilities. Action items: prepare detailed competitor feature comparison matrix and draft multi-year pricing proposals with various discount scenarios.', 'DataDriven Co', 'Demo', 'James Wilson', '2024-01-19 13:30:00', 85000, 'Analytics Pro'),
                ('CONV006', 'Extended technical deep dive with HealthTech Solutions'' IT Security team, Compliance Officer, and System Architects. Four-hour session focused on API infrastructure, data security protocols, and compliance requirements. Team raised specific concerns about HIPAA compliance, data encryption standards, and API rate limiting. Detailed discussion of our security architecture, including: end-to-end encryption, audit logging, and disaster recovery protocols. Client requires extensive documentation on compliance certifications, particularly SOC 2 and HITRUST. Security team performed initial architecture review and requested additional information about: database segregation, backup procedures, and incident response protocols. Follow-up session scheduled with their compliance team next week.', 'HealthTech Solutions', 'Technical Review', 'Rachel Torres', '2024-01-20 15:45:00', 120000, 'Premium Security'),
                ('CONV007', 'Contract review meeting with LegalEase Corp''s General Counsel, Procurement Director, and IT Manager. Detailed analysis of SLA terms, focusing on uptime guarantees and support response times. Legal team requested specific modifications to liability clauses and data handling agreements. Procurement raised questions about payment terms and service credit structure. Key discussion points included: disaster recovery commitments, data retention policies, and exit clause specifications. IT Manager confirmed technical requirements are met pending final security assessment. Agreement reached on most terms, with only SLA modifications remaining for discussion. Legal team to provide revised contract language by end of week. Overall positive session with clear path to closing.', 'LegalEase Corp', 'Negotiation', 'Mike Chen', '2024-01-21 10:00:00', 95000, 'Enterprise Suite'),
                ('CONV008', 'Quarterly business review with GlobalTrade Inc''s current implementation team and potential expansion stakeholders. Current implementation in Finance department showcasing strong adoption rates and 40% improvement in processing times. Discussion focused on expanding solution to Operations and HR departments. Users highlighted positive experiences with customer support and platform stability. Challenges identified in current usage: need for additional custom reports and increased automation in workflow processes. Expansion requirements gathered from Operations Director: inventory management integration, supplier portal access, and enhanced tracking capabilities. HR team interested in recruitment and onboarding workflow automation. Next steps: prepare department-specific implementation plans and ROI analysis for expansion.', 'GlobalTrade Inc', 'Expansion', 'James Wilson', '2024-01-22 14:20:00', 45000, 'Basic Package'),
                ('CONV009', 'Emergency planning session with FastTrack Ltd''s Executive team and Project Managers. Critical need for rapid implementation due to current system failure. Team willing to pay premium for expedited deployment and dedicated support team. Detailed discussion of accelerated implementation timeline and resource requirements. Key requirements: minimal disruption to operations, phased data migration, and emergency support protocols. Technical team confident in meeting aggressive timeline with additional resources. Executive sponsor emphasized importance of going live within 30 days. Immediate next steps: finalize expedited implementation plan, assign dedicated support team, and begin emergency onboarding procedures. Team to reconvene daily for progress updates.', 'FastTrack Ltd', 'Closing', 'Sarah Johnson', '2024-01-23 16:30:00', 180000, 'Premium Security'),
                ('CONV010', 'Quarterly strategic review with UpgradeNow Corp''s Department Heads and Analytics team. Current implementation meeting basic needs but team requiring more sophisticated analytics capabilities. Deep dive into current usage patterns revealed opportunities for workflow optimization and advanced reporting needs. Users expressed strong satisfaction with platform stability and basic features, but requiring enhanced data visualization and predictive analytics capabilities. Analytics team presented specific requirements: custom dashboard creation, advanced data modeling tools, and integrated BI features. Discussion about upgrade path from current package to Analytics Pro tier. ROI analysis presented showing potential 60% improvement in reporting efficiency. Team to present upgrade proposal to executive committee next month.', 'UpgradeNow Corp', 'Expansion', 'Rachel Torres', '2024-01-24 11:45:00', 65000, 'Analytics Pro')
                """).collect()
                st.success("✓ Step 2 complete! Table created with 10 comprehensive conversation transcripts")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Step 3: Cortex Search
    st.markdown("---\n### Step 3: Create Cortex Search Service")
    st.info("**Cortex Search** creates a semantic search index on your text data.\nThis enables the agent to find relevant conversations based on meaning, not just keywords.")
    setup_step3 = f"""-- Enable change tracking (required for Cortex Search)
ALTER TABLE "{db_name}"."{schema_name}".SALES_CONVERSATIONS SET CHANGE_TRACKING = TRUE;

-- Create Cortex Search service
CREATE CORTEX SEARCH SERVICE IF NOT EXISTS "{db_name}"."{schema_name}".{search_service}
  ON transcript_text 
  ATTRIBUTES customer_name, deal_stage, sales_rep 
  WAREHOUSE = COMPUTE_WH 
  TARGET_LAG = '1 hour'
  AS (
    SELECT transcript_text, customer_name, deal_stage, sales_rep, conversation_date
    FROM "{db_name}"."{schema_name}".SALES_CONVERSATIONS 
    WHERE conversation_date >= '2024-01-01'
  );"""
    st.code(setup_step3, language="sql")
    
    if st.button(":material/play_arrow: Run Step 3", key="run_step3", use_container_width=True):
        with st.status("Setting up Cortex Search...", expanded=True) as status:
            try:
                # Check if service already exists
                st.write(":material/search: Checking for existing search service...")
                try:
                    existing = session.sql(f'SHOW CORTEX SEARCH SERVICES IN SCHEMA "{db_name}"."{schema_name}"').collect()
                    service_exists = any(row['name'] == search_service for row in existing)
                except:
                    service_exists = False
                
                if service_exists:
                    st.write(f":material/check_circle: Search service '{search_service}' already exists")
                    status.update(label="✓ Step 3 complete (service already exists)!", state="complete")
                else:
                    # Enable change tracking
                    st.write(":material/update: Enabling change tracking...")
                    session.sql(f'ALTER TABLE "{db_name}"."{schema_name}".SALES_CONVERSATIONS SET CHANGE_TRACKING = TRUE').collect()
                    
                    # Create search service
                    st.write(":material/build: Creating Cortex Search service (30-60 seconds)...")
                    session.sql(f"""CREATE CORTEX SEARCH SERVICE "{db_name}"."{schema_name}".{search_service}
                        ON transcript_text 
                        ATTRIBUTES customer_name, deal_stage, sales_rep 
                        WAREHOUSE = COMPUTE_WH 
                        TARGET_LAG = '1 hour'
                        AS (
                          SELECT transcript_text, customer_name, deal_stage, sales_rep, conversation_date
                          FROM "{db_name}"."{schema_name}".SALES_CONVERSATIONS 
                          WHERE conversation_date >= '2024-01-01'
                        )""").collect()
                    
                    st.write(":material/check_circle: Search service created!")
                    status.update(label="✓ Step 3 complete! Indexing in background (1-2 min)", state="complete")
            except Exception as e:
                st.error(f"Error: {e}")
                status.update(label="Failed", state="error")
    
    # Step 4: Verification
    st.markdown("---\n### Step 4: Verify Setup")
    if st.button(":material/verified: Check if Ready for Day 27", type="primary", use_container_width=True):
        with st.status("Verifying setup...", expanded=True) as status:
            all_good = True
            
            # Check database
            try:
                result = session.sql(f'SHOW DATABASES LIKE \'{db_name}\'').collect()
                if result:
                    st.write(f":material/check_circle: Database exists")
                else:
                    st.write(f":material/cancel: Database not found")
                    all_good = False
            except Exception as e:
                st.write(f":material/cancel: Database check failed")
                all_good = False
            
            # Check table
            try:
                result = session.sql(f'SELECT COUNT(*) as cnt FROM "{db_name}"."{schema_name}".SALES_CONVERSATIONS').collect()
                st.write(f":material/check_circle: Conversations table with {result[0]['CNT']} records")
            except Exception as e:
                st.write(f":material/cancel: Conversations table not found")
                all_good = False
            
            # Check search service
            try:
                existing = session.sql(f'SHOW CORTEX SEARCH SERVICES IN SCHEMA "{db_name}"."{schema_name}"').collect()
                found = any(row['name'] == search_service for row in existing)
                if found:
                    st.write(f":material/check_circle: Cortex Search service exists")
                else:
                    st.write(f":material/cancel: Search service not found")
                    all_good = False
            except Exception as e:
                st.write(f":material/cancel: Search service check failed")
                all_good = False
            
            if all_good:
                status.update(label=":material/celebration: Ready for Day 27!", state="complete")
                st.balloons()
            else:
                status.update(label="Some checks failed - see details above", state="error")

# Create Agent Tab
with tab1:
    st.markdown("### Create Sales Conversation Agent")
    st.info("⚠️ **Note:** Cortex Agents may not be available in all Snowflake accounts yet. If you see errors, this feature might not be enabled for your account.")
    
    instructions = """You are a Sales Intelligence Assistant with access to sales conversation transcripts via the ConversationSearch tool.

IMPORTANT CONSTRAINTS:
- ONLY answer questions about sales conversations, deals, customers mentioned in transcripts
- DECLINE questions about: weather, coding, general knowledge, current events, or any non-sales topics
- Use ONLY the data from ConversationSearch - do NOT make up information
- If data is not found, clearly state that no conversation data is available"""
    
    create_sql = f"""CREATE OR REPLACE AGENT "{db_name}"."{schema_name}".{agent_name}
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-5
  instructions:
    response: '{instructions.replace("'", "''")}'
    orchestration: 'Use ConversationSearch to find relevant sales conversations. Decline off-topic questions politely.'
    system: 'You are a sales intelligence assistant. Answer ONLY from conversation data.'
  tools:
    - tool_spec:
        type: "cortex_search"
        name: "ConversationSearch"
        description: "Searches sales conversation transcripts"
  tool_resources:
    ConversationSearch:
      name: "{db_name}.{schema_name}.{search_service}"
      max_results: "5"
  $$;"""
    
    st.code(create_sql, language="sql")
    
    if st.button(":material/play_arrow: Create Agent", type="primary", use_container_width=True):
        with st.status("Creating agent...", expanded=True) as status:
            try:
                # Check if Cortex Agents available
                try:
                    session.sql("SHOW AGENTS").collect()
                    st.write(":material/check: Cortex Agents available")
                except Exception as e:
                    if "syntax error" in str(e).lower() or "does not exist" in str(e).lower():
                        st.error(":material/error: Cortex Agents not available in your account")
                        st.info("💡 This is a preview feature. Contact Snowflake support to enable it.")
                        status.update(label="Feature not available", state="error")
                        st.stop()
                    raise e
                
                # Create agent
                st.write(":material/build: Creating agent...")
                session.sql(create_sql).collect()
                st.write(f":material/check_circle: Agent created: {db_name}.{schema_name}.{agent_name}")
                st.session_state.agent_created = True
                status.update(label=":material/check_circle: Agent Ready for Day 27!", state="complete")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {str(e)}")
                status.update(label="Failed", state="error")

st.divider()
st.caption("Day 26: Introduction to Cortex Agents | 30 Days of AI with Streamlit")