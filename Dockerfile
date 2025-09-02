FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python code and all folders containing CSV/data
COPY main3.py .
COPY adv_comp/ adv_comp/
COPY apis/ apis/
COPY comp/ comp/
COPY services/ services/
COPY static/ static/

# Copy all data-related folders explicitly
COPY data/ data/
COPY KPI_Data/ KPI_Data/
COPY H_adv_analysis_data/ H_adv_analysis_data/
COPY H_adv_analysis_kpi/ H_adv_analysis_kpi/
COPY Market_data/ Market_data/
COPY output/ output/
COPY outputs/ outputs/
COPY PhysicalKPI/ PhysicalKPI/
COPY PhysicalKPICSV/ PhysicalKPICSV/
COPY SectionC/ SectionC/
COPY sectionCdata/ sectionCdata/
COPY section_Fcode/ section_Fcode/
COPY section_FCSV/ section_FCSV/
COPY SWOTdata/ SWOTdata/
COPY SWOTkpi/ SWOTkpi/

# (Optional) add image assets if needed
COPY bar_chart.png .
COPY platform_funnel_kpi_chart.png .
COPY purchase_frequency_mentions.png .

# Environment variable for real-time output
ENV PYTHONUNBUFFERED=1

# Expose FastAPI default port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main3:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
