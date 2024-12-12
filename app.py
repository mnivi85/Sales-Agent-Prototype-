import streamlit as st
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


# Model and Agent tools
llm =  ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"), model="llama3-8b-8192")
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()
# tools = [search] # add tools to the list

# Page Header
st.title("AI Sales Assistant Agent")
st.markdown("Assistant Agent Powered by Groq for product marketing.")



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
4. A tailored pitch strategy for the product name.
5. "Act as a sales agent crafting a professional and persuasive pitch for [Target Company]. The goal is to sell [Product Name], an innovative solution designed to address [specific problem or need].
[Target Company] is known for its commitment to [specific goals or values, e.g., sustainability, innovation, efficiency], making them an ideal customer for this product. The pitch should:
Emphasize the features and benefits of [Product Name] tailored for [Target Company]'s needs.
Highlight its superior performance compared to competitors like [Competitor A] and [Competitor B].
Address the company’s goals, including [specific goals such as cost reduction, environmental impact, or improving operational efficiency].
Include a comparison table showcasing key differentiators.
Conclude with a compelling call to action, inviting [Target Company] to pilot the product in their operations.
Use the following product details:
[Product Name] Features:
[Feature 1 and its benefit].
[Feature 2 and its benefit].
[Feature 3 and its benefit].
Competitor Information:
[Competitor A]: [Feature comparison].
[Competitor B]: [Feature comparison].
[Target Company] Goals:
[Goal 1 and how the product addresses it].
[Goal 2 and how the product supports it].

Draft and Create a structured pitch with sections for introduction, product advantages, competitor comparison, alignment with the company’s goals, and a call to action. close the pitch with thank you note and best regards, Sales Agent name."
Ensure that all sources (e.g., articles, press releases) are included in the output.


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

