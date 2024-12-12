import streamlit as st
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


# Model and Agent tools
llm =  ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"))
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()
# tools = [search] # add tools to the list

# Page Header
st.title("Smart Compost Bin Assistant Agent")
st.markdown("Assistant Agent Powered by Groq for Smart Compost Bin insights.")


# Data collection/inputs
with st.form("company_info", clear_on_submit=True):

  product_name = st.text_input("Product Name", "")
  product_category = st.text_input("Product Category", "")
  value_proposition = st.text_area("Value Proposition", "")
  company_url = st.text_input("Target Company URL", "")
  target_customer = st.text_input("Target Customer Name", "")
  uploaded_file = st.file_uploader("Upload Product Overview (Optional)", type=["pdf", "docx"])
  competitor_urls = st.text_area("Competitor URLs", "")

  # For the llm insights result
  company_insights = ""

  # Data process
  if st.form_submit_button("Generate Insights"):
    if product_name and company_url:
      st.spinner("Processing...")

      # search internet
      company_data = search.invoke(company_url)
      print(company_data)

      prompt = """
      
You are an AI assistant for sales representatives. Analyze the following information to provide actionable insights:


    Product Name: {product_name}
    Product Category: {product_category}
    Value Proposition: {value_proposition}
    Company Information: {company_data}
    Competitor URLs: {competitor_urls}
    Target Customer: {target_customer}
    Sales Agent name: {{"Nivitha"}}


Generate a report including:
1. The target company's strategy and recent activities.
2. Competitors' presence and their relation to the target company.
3. Key decision-makers at the target company.
4. A tailored pitch strategy for the product.
5."Act as a sales agent crafting a professional and persuasive pitch for Unilever. The goal is to sell the Smart Compost Bin, an advanced and eco-friendly waste management solution.

Unilever is committed to sustainability, waste reduction, and achieving net-zero goals, making them an ideal target customer. The pitch should:

Emphasize the features and benefits of the Smart Compost Bin tailored for Unilever's corporate needs.
Highlight its superior performance compared to competitors like Lomi by Pela and Vitamix FoodCycler.
Address Unilever’s sustainability goals, including waste reduction, energy efficiency, and community engagement.
Include a comparison table showcasing key differentiators.
Conclude with a call to action, inviting Unilever to pilot the product in their facilities.
Use the following product details:

Smart Compost Bin Features:

Processes food waste in 3-5 hours (faster than Lomi and Vitamix).
AI-powered insights into waste patterns.
Scalable design for high-volume usage (suitable for corporate cafeterias and offices).
Multi-layer odor control system with proprietary enzymes.
30% more energy-efficient than competitors.
Customizable branding and community engagement integration.
Competitor Information:

Lomi by Pela: Household-focused, 20-hour processing time, carbon filter for odor control.
Vitamix FoodCycler: Household-focused, 6-8 hours processing time, limited odor control.
Unilever’s Sustainability Goals:

Reduce landfill waste.
Optimize ESG reporting with measurable waste reduction.
Promote a circular economy and community engagement through waste repurposing.
Create a professional pitch with clear sections for introduction, product advantages,include comparison with competitors, alignment with Unilever’s goals, and a compelling call to action."


Provide the insights in a structured format.
"""
      

      # Prompt Template
      prompt_template = ChatPromptTemplate([("system", prompt)])

      # Chain
      chain = prompt_template | llm | parser

      # Result/Insights
      company_insights = chain.invoke({"company_data": company_data, "product_name": product_name, "product_category": product_category,"competitor_urls": competitor_urls, "value_proposition": value_proposition, "target_customer": target_customer}) 
      
# Add an alert when insights are ready
st.success("Insights generated successfully!")

# Display insights               
st.markdown(company_insights)




