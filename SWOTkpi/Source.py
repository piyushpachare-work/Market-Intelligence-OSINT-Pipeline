import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
import re
import numpy as np
from datetime import datetime
from fastapi.responses import JSONResponse
from wordcloud import WordCloud

# All your function definitions go here, e.g.:
def analyze_review_themes():
    """
    Analyze customer review themes from a hardcoded CSV file.
    Returns charts as base64 images and structured theme data.
    """
    try:
        # 🔗 Hardcoded CSV path (update this for production)
        KPI65_PATH = 'SWOTdata/KPI 65 - Sheet1.csv'

        # ✅ Load and process the CSV
        df = pd.read_csv(KPI65_PATH).dropna()
        total = df['Count'].sum()
        df['Percentage'] = (df['Count'] / total * 100).round(2)
        df = df.sort_values('Count', ascending=False)

        # 📊 Bar Chart
        plt.figure(figsize=(10, 6))
        df.plot(kind='bar', x='Theme', y='Count', legend=False, color='coral')
        plt.title('Negative Review Themes Frequency')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        bar_img = io.BytesIO()
        plt.savefig(bar_img, format='png')
        bar_img.seek(0)
        plt.close()

        # 🥧 Pie Chart
        plt.figure(figsize=(8, 8))
        df.plot(kind='pie', y='Count', labels=df['Theme'], autopct='%1.1f%%', legend=False, colormap='Set3')
        plt.title('Negative Review Themes Distribution')
        plt.ylabel('')
        plt.tight_layout()

        pie_img = io.BytesIO()
        plt.savefig(pie_img, format='png')
        pie_img.seek(0)
        plt.close()

        # 🔁 Convert images to base64
        bar_base64 = base64.b64encode(bar_img.getvalue()).decode('utf-8')
        pie_base64 = base64.b64encode(pie_img.getvalue()).decode('utf-8')

        # 📦 Structured response
        return {
            "status": "success",
            "kpi": "Negative Review Theme Analysis (KPI-82)",
            "charts": {
                "bar_chart": f"data:image/png;base64,{bar_base64}",
                "pie_chart": f"data:image/png;base64,{pie_base64}"
            },
            "table": df.to_dict(orient='records'),
            "markdown_table": df.to_markdown(index=False),
            "meta": {
                "total_themes": len(df),
                "date_generated": datetime.now().strftime("%Y-%m-%d")
            }
        }

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": f"Error processing file: {str(e)}"}
        )

# Weakness - 2. Lower Engagement Rate vs. Select Competitors
def analyze_social_media_metrics():
    """
    Analyze social media engagement and website bounce rates from local CSVs.
    Returns base64 images of visualizations and merged data table.
    """
    try:
        # 📁 Hardcoded file paths (update if needed)
        engagement_path = 'SWOTdata/KPI50 - Sheet1.csv'
        bounce_path = 'SWOTdata/KPI28 - Sheet1.csv'

        # ✅ Load and process engagement data
        engagement = pd.read_csv(engagement_path, skiprows=1).dropna().reset_index(drop=True)
        engagement['Followers'] = engagement['Followers'].str.replace('K', '').astype(float) * 1000
        engagement = engagement.rename(columns={engagement.columns[0]: "Company"})

        # ✅ Load and process bounce rate data
        bounce = pd.read_csv(bounce_path, skiprows=12).dropna().reset_index(drop=True)
        bounce['Bounce Rate (%)'] = bounce['Bounce Rate (%)'].str.replace('%', '').astype(float)
        bounce = bounce.rename(columns={bounce.columns[0]: "Company"})

        # 🔀 Merge data
        combined = pd.merge(engagement, bounce, on="Company", how='outer')

        # 📊 Chart 1: Engagement Rate
        plt.figure(figsize=(10, 6))
        combined.sort_values('Engagement Rate (%)', ascending=False).plot(
            kind='bar', x="Company", y='Engagement Rate (%)', legend=False, color='skyblue')
        plt.title('Social Media Engagement Rate Comparison')
        plt.ylabel('Engagement Rate (%)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        engagement_img = io.BytesIO()
        plt.savefig(engagement_img, format='png')
        engagement_img.seek(0)
        plt.close()

        # 📊 Chart 2: Bounce Rate
        plt.figure(figsize=(10, 6))
        combined.dropna(subset=['Bounce Rate (%)']).sort_values('Bounce Rate (%)').plot(
            kind='bar', x="Company", y='Bounce Rate (%)', legend=False, color='salmon')
        plt.title('Website Bounce Rate Comparison')
        plt.ylabel('Bounce Rate (%)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        bounce_img = io.BytesIO()
        plt.savefig(bounce_img, format='png')
        bounce_img.seek(0)
        plt.close()

        # 🧬 Encode images
        engagement_base64 = base64.b64encode(engagement_img.getvalue()).decode('utf-8')
        bounce_base64 = base64.b64encode(bounce_img.getvalue()).decode('utf-8')

        # 📦 Response
        return {
            "status": "success",
            "kpi": "Social Media & Website Bounce Analysis (KPI-8)",
            "charts": {
                "engagement_rate_chart": f"data:image/png;base64,{engagement_base64}",
                "bounce_rate_chart": f"data:image/png;base64,{bounce_base64}"
            },
            "table": combined[[
                "Company", "Followers", "Avg Likes/Post", "Avg Comments/Post",
                "Engagement Rate (%)", "Bounce Rate (%)"
            ]].to_dict(orient='records'),
            "markdown_table": combined[[
                "Company", "Followers", "Avg Likes/Post", "Avg Comments/Post",
                "Engagement Rate (%)", "Bounce Rate (%)"
            ]].to_markdown(index=False),
            "meta": {
                "companies_analyzed": len(combined),
                "generated_on": datetime.now().strftime("%Y-%m-%d")
            }
        }

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": f"Error processing data: {str(e)}"}
        )
    

# Weakness - 3. Identified Website Usability Issues
def analyze_website_issues():
    """
    Analyze PageSpeed and mobile-friendliness from local CSV files.
    Returns base64 images of charts and structured metrics.
    """
    try:
        # 📁 File paths for KPI58 and KPI59
        KPI59_PATH = 'SWOTdata/KPI59 - Sheet1.csv'  # PageSpeed
        KPI58_PATH = 'SWOTdata/KPI58 - Sheet1.csv'  # Mobile

        # ✅ Load PageSpeed data (skiprows=2 to skip headers)
        pagespeed = pd.read_csv(KPI59_PATH, skiprows=2).dropna()

        # ✅ Construct Mobile Data manually (or from file if needed)
        mobile_data = {
            'Component': ['Responsive Design', 'Readable Text', 'Touch Elements', 
                          'Viewport Configuration', 'Load Performance'],
            'Assessment': ['Optimal', 'Appropriate', 'Adequate', 'Proper', 'Efficient'],
            'Score': [90, 95, 80, 100, 85]
        }
        mobile_df = pd.DataFrame(mobile_data)

        # 📊 Plot 1: PageSpeed comparison
        plt.figure(figsize=(10, 6))
        pagespeed.plot(kind='bar', x='Metric', y=['Desktop Score', 'Mobile Score'], color=['#4caf50', '#2196f3'])
        plt.title('PageSpeed Insights Scores Comparison')
        plt.ylabel('Score (0–100)')
        plt.ylim(0, 110)
        plt.legend(['Desktop', 'Mobile'])
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        pagespeed_img = io.BytesIO()
        plt.savefig(pagespeed_img, format='png')
        pagespeed_img.seek(0)
        plt.close()

        # 📊 Plot 2: Mobile Friendliness Score
        plt.figure(figsize=(10, 6))
        mobile_df.plot(kind='barh', x='Component', y='Score', legend=False, color='orange')
        plt.title('Mobile-Friendliness Components Assessment')
        plt.xlabel('Score (0–100)')
        plt.xlim(0, 110)
        plt.tight_layout()

        mobile_img = io.BytesIO()
        plt.savefig(mobile_img, format='png')
        mobile_img.seek(0)
        plt.close()

        # 🧬 Data merge for response
        pagespeed['Mobile-Friendly Assessment'] = '-'
        pagespeed['Component Score'] = '-'

        mobile_df['Desktop Score'] = '-'
        mobile_df['Mobile Score'] = '-'

        combined = pd.concat([
            pagespeed[['Metric', 'Desktop Score', 'Mobile Score', 
                       'Mobile-Friendly Assessment', 'Component Score']],
            mobile_df[['Component', 'Desktop Score', 'Mobile Score', 
                       'Assessment', 'Score']].rename(columns={
                           'Component': 'Metric',
                           'Assessment': 'Mobile-Friendly Assessment',
                           'Score': 'Component Score'
                       })
        ], ignore_index=True)

        # 🔁 Convert to base64
        pagespeed_base64 = base64.b64encode(pagespeed_img.getvalue()).decode('utf-8')
        mobile_base64 = base64.b64encode(mobile_img.getvalue()).decode('utf-8')

        # 📦 Final response
        return {
            "status": "success",
            "kpi": "PageSpeed & Mobile-Friendliness Metrics (KPI-58, KPI-59)",
            "charts": {
                "pagespeed_chart": f"data:image/png;base64,{pagespeed_base64}",
                "mobile_chart": f"data:image/png;base64,{mobile_base64}"
            },
            "table": combined.to_dict(orient='records'),
            "markdown_table": combined.to_markdown(index=False),
            "meta": {
                "metrics_analyzed": len(combined),
                "generated_on": datetime.now().strftime("%Y-%m-%d")
            }
        }

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": f"Error processing metrics: {str(e)}"}
        )

#Weakness - 4. Gaps in Online Customer Service Response
sns.set(style="whitegrid")
KPI66 = "SWOTdata/KPI66 - Haldiram Response Rate.csv"

async def analyze_response_rates():
    """
    Endpoint to analyze customer service response rates by platform.
    Uses a predefined file path (hardcoded in the application).
    Returns visualizations, analysis results, and the processed data.
    """
    try:
        # Load and process the data
        df_raw = pd.read_csv(KPI66, skip_blank_lines=False)
        
        # Clean the data
        df = df_raw.dropna(how='all').dropna(axis=1, how='all')
        df = df.iloc[1:].reset_index(drop=True)
        df.columns = ['Platform', 'No. of Reviews Checked', 'Percentage of Reviews with Responses']
        df = df[df['Platform'].notna() & (df['Platform'] != '')]
        
        # Convert data types
        df['No. of Reviews Checked'] = df['No. of Reviews Checked'].astype(int)
        df['Response Rate (%)'] = df['Percentage of Reviews with Responses'].str.replace('%', '').astype(float)
        df = df[['Platform', 'No. of Reviews Checked', 'Response Rate (%)']]
        
        # Calculate metrics
        min_rate = df['Response Rate (%)'].min()
        max_rate = df['Response Rate (%)'].max()
        gap = max_rate - min_rate
        lowest_platforms = df[df['Response Rate (%)'] == min_rate]['Platform'].tolist()
        
        # Create visualization
        plt.figure(figsize=(8, 5))
        sns.barplot(
            data=df,
            x='Platform',
            y='Response Rate (%)',
            palette='Blues_d'
        )
        plt.title('Customer Service Response Rates by Platform')
        plt.ylabel('Response Rate (%)')
        plt.xlabel('Platform')
        plt.ylim(0, 100)
        plt.tight_layout()
        
        # Save plot to bytes
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        plt.close()
        
        # Convert image to base64
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        # Prepare response
        return {
            "visualization": f"data:image/png;base64,{img_base64}",
            "analysis": {
                "highest_response_rate": max_rate,
                "lowest_response_rate": min_rate,
                "response_rate_gap": gap,
                "lowest_response_platforms": lowest_platforms
            },
            "data": df.to_dict(orient='records'),
            "markdown_table": df.to_markdown(index=False)
        }
    
    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"message": f"File not found at path: {KPI66}. Please check the file path in the application code."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing data: {str(e)}"}
        )


# Weakness - 5. Negative News Sentiment Spikes 
KPI61 = "SWOTdata/KPI61 - Sheet1.csv"
async def news_sentiment_spikes():
    """
    Endpoint to perform sentiment analysis on news data.
    Uses a predefined file path (hardcoded in the application).
    Returns visualizations, analysis results, and negative headlines.
    """
    try:
        # Load and clean data
        df = pd.read_csv(KPI61)
        df = df.dropna()
        df['Sentiment Score (-1 to +1)'] = pd.to_numeric(df['Sentiment Score (-1 to +1)'])

        # Sentiment analysis
        sentiment_counts = df['Overall Sentiment'].value_counts()
        sentiment_percent = df['Overall Sentiment'].value_counts(normalize=True) * 100
        avg_scores = df.groupby('Overall Sentiment')['Sentiment Score (-1 to +1)'].mean()

        # Create results table
        results = pd.DataFrame({
            'Count': sentiment_counts,
            'Percentage': sentiment_percent.round(2),
            'Avg. Sentiment Score': avg_scores.round(2)
        })

        # Get negative headlines
        negative_news = df[df['Overall Sentiment'] == 'Negative'][['Headline', 'Sentiment Score (-1 to +1)']]

        # Create visualizations
        # Visualization 1: Pie chart
        plt.figure(figsize=(8, 8))
        df['Overall Sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Sentiment Distribution')
        plt.ylabel('')
        plt.tight_layout()
        
        pie_img = io.BytesIO()
        plt.savefig(pie_img, format='png')
        pie_img.seek(0)
        plt.close()

        # Visualization 2: Histogram
        plt.figure(figsize=(10, 6))
        df['Sentiment Score (-1 to +1)'].hist(bins=20)
        plt.title('Sentiment Score Distribution')
        plt.xlabel('Sentiment Score (-1 to +1)')
        plt.ylabel('Number of Articles')
        plt.tight_layout()
        
        hist_img = io.BytesIO()
        plt.savefig(hist_img, format='png')
        hist_img.seek(0)
        plt.close()

        # Convert images to base64
        pie_base64 = base64.b64encode(pie_img.getvalue()).decode('utf-8')
        hist_base64 = base64.b64encode(hist_img.getvalue()).decode('utf-8')

        # Prepare response
        return {
            "visualizations": {
                "sentiment_distribution": f"data:image/png;base64,{pie_base64}",
                "score_distribution": f"data:image/png;base64,{hist_base64}"
            },
            "analysis_results": {
                "sentiment_distribution": results.to_dict(orient='index'),
                "negative_headlines": negative_news.to_dict(orient='records')
            },
            "formatted_outputs": {
                "sentiment_table": results.to_markdown(),
                "negative_headlines_table": negative_news.to_markdown(index=False)
            }
        }
    
    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"message": f"File not found at path: {KPI61}. Please check the file path in the application code."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing data: {str(e)}"}
        )
    
#Strengths KPI - 1. High Brand Search Volume Rank
KPI41_PATH = "SWOTdata/KPI41 - Sheet1.csv"
KPI42_PATH = "SWOTdata/KPI42 - Sheet1.csv"
async def search_volume_rank():
    """
    Endpoint to perform brand awareness analysis.
    Uses predefined file paths (hardcoded in the application).
    Returns visualizations, analysis results, and key takeaways.
    """
    try:
        # ===== DATA PREPARATION =====
        kpi41 = pd.read_csv(KPI41_PATH, skiprows=1)
        kpi42 = pd.read_csv(KPI42_PATH, skiprows=1)
        
        # Get Share of Search
        share_of_search = float(kpi42.loc[kpi42['Brand'] == 'Haldiram', 'Share of Search %'].values[0].strip('%'))

        # Normalize 2025 Search Volume (0-100 scale)
        kpi41["2025_normalized"] = ((kpi41["2025"] - kpi41["2025"].min()) /
                                  (kpi41["2025"].max() - kpi41["2025"].min())) * 100

        # Combine Scores (50% normalized search volume + 50% share of search)
        kpi41["Combined_Score"] = (kpi41["2025_normalized"] * 0.5) + (share_of_search * 0.5)

        # Rank Countries (Higher score = Better brand awareness)
        kpi41["High_Brand_Search_Rank"] = kpi41["Combined_Score"].rank(ascending=False).astype(int)

        # Final Result (Sorted by Rank)
        result = kpi41[["Country", "2025", "2025_normalized", "Combined_Score", "High_Brand_Search_Rank"]].sort_values("High_Brand_Search_Rank")

        # ===== KEY TAKEAWAYS =====
        key_takeaways = [
            "1. USA is the Top-Performing Market",
            "   - Highest absolute search volume (83) in 2025.",
            "   - Combined with a strong 70% share of search, it ranks #1 in brand awareness.",
            "",
            "2. Australia, Canada, and India Show Strong Growth",
            "   - All three have high normalized search volumes (76.2, 71.4, 78.6).",
            "   - India has a slightly lower rank due to lower combined score despite high search volume.",
            "",
            "3. UK and UAE Lag Behind",
            "   - UK has moderate search volume (64.3 normalized) but lacks dominance.",
            "   - UAE has the lowest search volume (41), dragging its rank down despite a 70% share.",
            "",
            "4. Brand Awareness is Strongest in Western Markets",
            "   - USA, Australia, Canada dominate rankings, suggesting higher brand recognition in these regions.",
            "   - India, despite being Haldiram's home market, ranks 2nd, possibly due to saturation or competition.",
            "",
            "5. Opportunity for Improvement in UAE",
            "   - While Haldiram has a 70% search share, the absolute search volume is very low (41).",
            "   - Potential for marketing campaigns to boost overall brand searches in the UAE."
        ]

        # ===== VISUALIZATIONS =====
        sns.set_theme()
        plt.figure(figsize=(15, 10))

        # Create a dictionary to store all visualizations
        visualizations = {}

        # Visualization 1: Combined Score Bar Chart
        plt.subplot(2, 2, 1)
        sns.barplot(data=result, x='Combined_Score', y='Country', palette='viridis')
        plt.title('Brand Awareness Score by Country (2025)')
        plt.xlabel('Combined Score')
        plt.ylabel('Country')
        for index, value in enumerate(result['Combined_Score']):
            plt.text(value, index, f'{value:.1f}')
        
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight')
        img1.seek(0)
        visualizations["score_bar_chart"] = f"data:image/png;base64,{base64.b64encode(img1.getvalue()).decode('utf-8')}"
        plt.clf()

        # Visualization 2: Search Volume Trend Heatmap
        plt.subplot(2, 2, 2)
        trend_data = kpi41.set_index('Country')[['2021', '2022', '2023', '2024', '2025']]
        sns.heatmap(trend_data, annot=True, cmap='YlOrRd', fmt='g')
        plt.title('Search Volume Trend (2021-2025)')
        plt.ylabel('Country')
        
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight')
        img2.seek(0)
        visualizations["trend_heatmap"] = f"data:image/png;base64,{base64.b64encode(img2.getvalue()).decode('utf-8')}"
        plt.clf()

        # Visualization 3: Rank Comparison
        plt.subplot(2, 2, 3)
        rank_data = result[['Country', 'High_Brand_Search_Rank']].sort_values('High_Brand_Search_Rank')
        sns.barplot(data=rank_data, x='High_Brand_Search_Rank', y='Country', palette='rocket')
        plt.title('Brand Search Ranking (2025)')
        plt.xlabel('Rank (1 = Best)')
        for index, value in enumerate(rank_data['High_Brand_Search_Rank']):
            plt.text(value, index, str(value))
        
        img3 = io.BytesIO()
        plt.savefig(img3, format='png', bbox_inches='tight')
        img3.seek(0)
        visualizations["rank_comparison"] = f"data:image/png;base64,{base64.b64encode(img3.getvalue()).decode('utf-8')}"
        plt.clf()

        # Visualization 4: Normalized vs Absolute Search
        plt.subplot(2, 2, 4)
        plt.scatter(result['2025'], result['2025_normalized'], c=result['High_Brand_Search_Rank'], cmap='viridis', s=200)
        for i, txt in enumerate(result['Country']):
            plt.annotate(txt, (result['2025'][i], result['2025_normalized'][i]))
        plt.colorbar(label='Rank (Lower = Better)')
        plt.title('Absolute vs Normalized Search Volume')
        plt.xlabel('Absolute Search Volume (2025)')
        plt.ylabel('Normalized Search Volume (0-100)')
        
        img4 = io.BytesIO()
        plt.savefig(img4, format='png', bbox_inches='tight')
        img4.seek(0)
        visualizations["search_comparison"] = f"data:image/png;base64,{base64.b64encode(img4.getvalue()).decode('utf-8')}"
        plt.close()

        # Prepare response
        return {
            "analysis_results": {
                "data_table": result.to_dict(orient='records'),
                "formatted_table": result.to_markdown(index=False),
                "share_of_search": share_of_search,
                "key_takeaways": key_takeaways
            },
            "visualizations": visualizations
        }

    except FileNotFoundError as e:
        return JSONResponse(
            status_code=404,
            content={"message": f"File not found: {str(e)}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing data: {str(e)}"}
        )
    
#Strengths KPI - 2. Overall Positive Sentiment Score
KPI45_PATH = "SWOTdata/KPI45 - Sheet1.csv"

async def analyze_sentiment_score():
    """
    Calculates the Positive Overall Sentiment Score (POSS) from KPI45 CSV.
    Provides visualizations and sentiment interpretation.
    """
    try:
        # ===== LOAD & PREPARE DATA =====
        df = pd.read_csv(KPI45_PATH, skiprows=1)
        df['Percentage'] = df['Percentage'].str.rstrip('%').astype(float) / 100

        pos_pct = df[df['Sentiment'] == 'Positive']['Percentage'].values[0]
        neu_pct = df[df['Sentiment'] == 'Neutral']['Percentage'].values[0]
        neg_pct = df[df['Sentiment'] == 'Negative']['Percentage'].values[0]

        # ===== CALCULATE POSS =====
        positive_score = round((pos_pct * 1.0 + neu_pct * 0.3 - neg_pct * 0.7) * 100, 1)

        # ===== INTERPRETATION =====
        if positive_score >= 70:
            interpretation = 'Strong positive sentiment'
        elif positive_score >= 50:
            interpretation = 'Generally favorable sentiment'
        elif positive_score >= 30:
            interpretation = 'Mixed sentiment with some concerns'
        else:
            interpretation = 'Predominantly negative sentiment'

        result = pd.DataFrame({
            'KPI': ['Positive Overall Sentiment Score (POSS)'],
            'Score': [positive_score],
            'Interpretation': [interpretation],
            'Positive %': [pos_pct * 100],
            'Negative %': [neg_pct * 100],
            'Neutral %': [neu_pct * 100]
        })

        # ===== KEY TAKEAWAYS =====
        key_takeaways = [
            f"1. Overall Sentiment Score (POSS) is {positive_score}/100",
            f"2. {interpretation}",
            f"3. Sentiment breakdown:",
            f"   - Positive: {pos_pct * 100:.1f}%",
            f"   - Neutral: {neu_pct * 100:.1f}%",
            f"   - Negative: {neg_pct * 100:.1f}%"
        ]

        # ===== VISUALIZATIONS =====
        sns.set_theme()
        visualizations = {}

        # Pie Chart: Sentiment Distribution
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.pie(df['Percentage'], labels=df['Sentiment'],
                autopct='%1.1f%%', colors=['#4CAF50', '#F44336', '#FFC107'],
                startangle=90)
        plt.title('Sentiment Distribution')

        # Bar Chart: POSS
        plt.subplot(1, 2, 2)
        plt.barh(['POSS'], [positive_score], color='#2196F3')
        plt.xlim(0, 100)
        plt.title('Positive Overall Sentiment Score')
        plt.xlabel('Score (0-100)')

        # Save plot to buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        visualizations["sentiment_analysis"] = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
        plt.close()

        # ===== RETURN API RESPONSE =====
        return {
            "analysis_results": {
                "data_table": result.to_dict(orient='records'),
                "formatted_table": result.to_markdown(index=False),
                "positive_score": positive_score,
                "key_takeaways": key_takeaways
            },
            "visualizations": visualizations
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"message": f"File not found: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error processing data: {str(e)}"})
    
# Strengths KPI - 3. Wide Product Range Visibility
KPI20_PATH = "SWOTdata/KPI20 - Sheet1.csv"
KPI21_PATH = "SWOTdata/KPI21 - Sheet1.csv"
KPI68_PATH = "SWOTdata/KPI68 - Sheet1.csv"

async def product_range_visibility():
    """
    Combines KPI20, KPI21, KPI68 to analyze product category coverage,
    variant launches, and product rating insights.
    """
    try:
        # ===== LOAD & CLEAN DATA =====
        kpi20 = pd.read_csv(KPI20_PATH, skiprows=1).dropna()
        kpi21 = pd.read_csv(KPI21_PATH, skiprows=1)
        kpi68 = pd.read_csv(KPI68_PATH, skiprows=1)

        # Process KPI20: Category Breadth
        categories = ['NAMKEEN', 'SWEETS', 'FROZEN FOODS', 'BISCUITS', 'RTE', 'CHIPS']
        kpi20['Categories Covered'] = (kpi20[categories] > 0).sum(axis=1)

        # Process KPI21: New Variants
        kpi21_grouped = kpi21.groupby('Competitor')['Number of Variants/Flavors Launched'].sum().reset_index()

        # Process KPI68: Product Ratings
        avg_ratings = kpi68.groupby(kpi68.columns[0])['Overall Rating'].mean().reset_index()
        avg_ratings.columns = ['Brand', 'Avg. Product Rating']

        # Merge All
        combined = pd.merge(kpi20[['Brand', 'Categories Covered']], kpi21_grouped, left_on='Brand', right_on='Competitor', how='left')
        combined = pd.merge(combined, avg_ratings, on='Brand', how='left')
        combined = combined.drop(columns=['Competitor'])

        # ===== KEY TAKEAWAYS =====
        top_categories = combined.sort_values("Categories Covered", ascending=False).iloc[0]
        top_variants = combined.sort_values("Number of Variants/Flavors Launched", ascending=False).iloc[0]
        top_rated = avg_ratings.sort_values("Avg. Product Rating", ascending=False).iloc[0]

        key_takeaways = [
            f"1. {top_categories['Brand']} has the widest product category coverage ({int(top_categories['Categories Covered'])} categories).",
            f"2. {top_variants['Brand']} leads in launching new variants ({int(top_variants['Number of Variants/Flavors Launched'])} variants in Q1 2025).",
            f"3. {top_rated['Brand']} has the highest average product rating ({round(top_rated['Avg. Product Rating'], 2)} out of 5)."
        ]

        # ===== VISUALIZATIONS =====
        sns.set_theme()
        visualizations = {}

        def plot_to_base64(fig):
            buf = io.BytesIO()
            fig.tight_layout()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

        # Plot 1: Product Category Coverage
        fig1 = plt.figure(figsize=(12, 6))
        combined.sort_values('Categories Covered', ascending=False).plot(kind='bar', x='Brand', y='Categories Covered', legend=False, ax=fig1.gca())
        plt.title('Product Category Coverage Comparison')
        plt.ylabel('Number of Categories')
        visualizations['category_coverage'] = plot_to_base64(fig1)
        plt.close(fig1)

        # Plot 2: New Variant Launches
        fig2 = plt.figure(figsize=(12, 6))
        combined.sort_values('Number of Variants/Flavors Launched', ascending=False).plot(kind='bar', x='Brand', y='Number of Variants/Flavors Launched', legend=False, ax=fig2.gca())
        plt.title('New Variant Launches Comparison (Q1 2025)')
        plt.ylabel('Number of New Variants')
        visualizations['variant_launches'] = plot_to_base64(fig2)
        plt.close(fig2)

        # Plot 3: Product Ratings Distribution (Haldiram only)
        fig3 = plt.figure(figsize=(10, 6))
        haldiram_ratings = kpi68[kpi68[kpi68.columns[0]] == "Haldiram"]['Overall Rating']
        haldiram_ratings.hist(bins=10)
        plt.title("Haldiram's Product Ratings Distribution")
        plt.xlabel('Rating (1-5)')
        plt.ylabel('Number of Products')
        visualizations['product_ratings'] = plot_to_base64(fig3)
        plt.close(fig3)

        # ===== RETURN API RESPONSE =====
        return {
            "analysis_results": {
                "data_table": combined.to_dict(orient='records'),
                "formatted_table": combined.to_markdown(index=False),
                "key_takeaways": key_takeaways
            },
            "visualizations": visualizations
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"message": f"File not found: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error processing data: {str(e)}"})


# Strengths KPI - 4. Strong E-commerce Presence/Ratings
KPI24_PATH = 'SWOTdata/KPI24 - Sheet1.csv'
KPI63_PATH = 'SWOTdata/KPI63 - Sheet1.csv'

async def analyze_ecommerce_presence():
    """
    Combines KPI24 and KPI63 to analyze:
    - E-commerce platform coverage.
    - Rating strength based on reviews.
    """
    try:
        # ===== Load and Clean Data =====
        kpi24 = pd.read_csv(KPI24_PATH, skiprows=1)
        kpi24.columns = ['Brand', 'Amazon', 'Flipkart', 'BigBasket', 'Zepto', 'Swiggy Instamart', 'Own Website', 'Total Platforms', 'Distribution Reach']
        kpi24['E-commerce Presence'] = kpi24['Total Platforms'].apply(lambda x: 'Strong' if x >= 5 else 'Weak')

        kpi63 = pd.read_csv(KPI63_PATH, skiprows=1)
        kpi63.columns = ['Platform', 'Products', 'Shop Name', 'No. of Reviews', 'Location']

        kpi63_reviews = kpi63.groupby('Shop Name')['No. of Reviews'].sum().reset_index()
        kpi63_reviews['Rating Strength'] = kpi63_reviews['No. of Reviews'].apply(
            lambda x: 'Strong' if x > 1000 else 'Moderate' if x > 500 else 'Weak'
        )

        # ===== Merge =====
        merged = pd.merge(
            kpi24[['Brand', 'E-commerce Presence', 'Total Platforms']],
            kpi63_reviews,
            left_on='Brand',
            right_on='Shop Name',
            how='left'
        )
        final_kpi = merged[['Brand', 'E-commerce Presence', 'No. of Reviews', 'Rating Strength']]

        # ===== Takeaways =====
        takeaways = [
            "1. Brands with strong e-commerce presence (5+ platforms) dominate the online market.",
            "2. Few shops have strong ratings (1000+ reviews), showing a gap in customer engagement.",
            "3. Scatterplot reveals positive correlation between total platforms and number of reviews.",
            "4. Weak presence or low reviews mark improvement areas in digital outreach."
        ]

        # ===== VISUALIZATIONS =====
        sns.set_theme()
        visualizations = {}

        def plot_to_base64(fig):
            buf = io.BytesIO()
            fig.tight_layout()
            fig.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

        # Plot 1: E-commerce Presence Count
        fig1 = plt.figure(figsize=(10, 6))
        ax1 = sns.countplot(data=kpi24, x='E-commerce Presence', palette='coolwarm')
        plt.title('E-commerce Presence of Brands')
        plt.xlabel('E-commerce Presence')
        plt.ylabel('Number of Brands')
        for index, value in enumerate(kpi24['E-commerce Presence'].value_counts()):
            ax1.text(index, value + 0.5, str(value), ha='center')
        visualizations['ecommerce_presence_chart'] = plot_to_base64(fig1)
        plt.close(fig1)

        # Plot 2: Rating Strength Count
        fig2 = plt.figure(figsize=(10, 6))
        ax2 = sns.countplot(data=kpi63_reviews, x='Rating Strength', palette='viridis')
        plt.title('Rating Strength of Shops')
        plt.xlabel('Rating Strength')
        plt.ylabel('Number of Shops')
        for index, value in enumerate(kpi63_reviews['Rating Strength'].value_counts()):
            ax2.text(index, value + 0.5, str(value), ha='center')
        visualizations['rating_strength_chart'] = plot_to_base64(fig2)
        plt.close(fig2)

        # Plot 3: Platforms vs Reviews Scatterplot
        fig3 = plt.figure(figsize=(10, 6))
        scatter_data = pd.merge(kpi24[['Brand', 'Total Platforms', 'E-commerce Presence']], kpi63_reviews, left_on='Brand', right_on='Shop Name', how='left')
        sns.scatterplot(data=scatter_data, x='Total Platforms', y='No. of Reviews', hue='E-commerce Presence', palette='coolwarm', s=150)
        plt.title('Correlation Between Platforms and Reviews')
        plt.xlabel('Total Platforms')
        plt.ylabel('Number of Reviews')
        plt.legend(title='E-commerce Presence')
        visualizations['correlation_scatter'] = plot_to_base64(fig3)
        plt.close(fig3)

        return {
            "analysis_results": {
                "data_table": final_kpi.to_dict(orient="records"),
                "formatted_table": final_kpi.to_markdown(index=False),
                "key_takeaways": takeaways
            },
            "visualizations": visualizations
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"message": f"File not found: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error processing data: {str(e)}"})
# Strengths KPI - 5. High Review Volume
KPI62_PATH = "SWOTdata/KPI62 - Haldiram Online Review Volume.csv"

async def high_review_volume():
    try:
        # ===== DATA LOADING =====
        df = pd.read_csv(KPI62_PATH)

        # ===== SUMMARY CALCULATIONS =====
        amazon = df[df['Platform'] == 'Amazon (Products)']['No. of Reviews'].sum()
        flipkart = df[df['Platform'] == 'Flipkart (Products)']['No. of Reviews'].sum()
        google = df[df['Platform'] == 'Google Reviews (Mumbai)']['No. of Reviews'].sum()
        dining = df[df['Platform'] == 'Dining/Delivery']['No. of Reviews'].sum()
        total = df['Estimated Total Count (Google Reviews, Zomato, Swiggy, Amazon, Flipkart)'].max()

        summary = pd.DataFrame({
            'Platform': ['Amazon Products', 'Dining/Delivery', 'Flipkart Products', 
                         'Google Reviews', 'Total'],
            'Total Reviews': [amazon, dining, flipkart, google, total],
            'Percentage': [f"{(amazon/total)*100:.2f}%", f"{(dining/total)*100:.2f}%",
                           f"{(flipkart/total)*100:.2f}%", f"{(google/total)*100:.2f}%", "100%"],
            'Top Product/Location': [
                df[df['Platform'] == 'Amazon (Products)'].nlargest(1, 'No. of Reviews')['Products'].values[0],
                df[df['Platform'] == 'Dining/Delivery'].nlargest(1, 'No. of Reviews')['Location'].values[0],
                df[df['Platform'] == 'Flipkart (Products)'].nlargest(1, 'No. of Reviews')['Products'].values[0],
                df[df['Platform'] == 'Google Reviews (Mumbai)'].nlargest(1, 'No. of Reviews')['Location'].values[0],
                ''
            ],
            'Top Review Count': [
                df[df['Platform'] == 'Amazon (Products)']['No. of Reviews'].max(),
                df[df['Platform'] == 'Dining/Delivery']['No. of Reviews'].max(),
                df[df['Platform'] == 'Flipkart (Products)']['No. of Reviews'].max(),
                df[df['Platform'] == 'Google Reviews (Mumbai)']['No. of Reviews'].max(),
                ''
            ]
        })

        # ===== TOP 5 PRODUCTS =====
        top_products = df[df['Platform'].str.contains('Amazon|Flipkart', na=False)]\
            .nlargest(5, 'No. of Reviews')[['Products', 'Platform', 'No. of Reviews']]

        # ===== KEY TAKEAWAYS =====
        key_takeaways = [
            "1. Amazon and Flipkart dominate product reviews, showing strong e-commerce presence.",
            f"   - Amazon has {amazon} reviews, Flipkart has {flipkart}.",
            "   - Top reviewed product on Amazon: " + summary.loc[0, 'Top Product/Location'],
            "   - Top reviewed product on Flipkart: " + summary.loc[2, 'Top Product/Location'],
            "",
            f"2. Dining/Delivery platforms have {dining} reviews, mostly from key metro cities.",
            "   - Most reviewed dining location: " + summary.loc[1, 'Top Product/Location'],
            "",
            f"3. Google Reviews (Mumbai) contributes {google} reviews, showing strong local engagement.",
            "   - Most reviewed location: " + summary.loc[3, 'Top Product/Location'],
            "",
            f"4. Total online review volume: {int(total)} across all platforms."
        ]

        # ===== VISUALIZATIONS =====
        sns.set_theme()
        visualizations = {}

        # Pie Chart: Platform Review Share
        plt.figure(figsize=(7, 7))
        plt.pie(summary['Total Reviews'][:-1], labels=summary['Platform'][:-1], 
                autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
        plt.title("Platform-wise Review Distribution")
        plt.axis('equal')
        pie_img = io.BytesIO()
        plt.savefig(pie_img, format='png', bbox_inches='tight')
        pie_img.seek(0)
        visualizations["platform_pie_chart"] = f"data:image/png;base64,{base64.b64encode(pie_img.getvalue()).decode('utf-8')}"
        plt.clf()

        # Bar Chart: Top 5 Reviewed Products
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_products, x='No. of Reviews', y='Products', hue='Platform', palette='viridis')
        plt.title("Top 5 Reviewed Products (Amazon & Flipkart)")
        plt.xlabel("Number of Reviews")
        plt.ylabel("Product")
        bar_img = io.BytesIO()
        plt.savefig(bar_img, format='png', bbox_inches='tight')
        bar_img.seek(0)
        visualizations["top_products_bar"] = f"data:image/png;base64,{base64.b64encode(bar_img.getvalue()).decode('utf-8')}"
        plt.clf()

        # Bar Chart: Total Reviews by Platform
        plt.figure(figsize=(8, 5))
        sns.barplot(x=summary['Platform'][:-1], y=summary['Total Reviews'][:-1], palette='Set2')
        plt.title("Total Reviews by Platform")
        plt.xlabel("Platform")
        plt.ylabel("Total Reviews")
        plt.xticks(rotation=15)
        platform_bar_img = io.BytesIO()
        plt.savefig(platform_bar_img, format='png', bbox_inches='tight')
        platform_bar_img.seek(0)
        visualizations["platform_bar_chart"] = f"data:image/png;base64,{base64.b64encode(platform_bar_img.getvalue()).decode('utf-8')}"
        plt.close()

        return {
            "review_summary": {
                "data_table": summary.to_dict(orient="records"),
                "formatted_table": summary.to_markdown(index=False),
                "key_takeaways": key_takeaways,
                "top_5_reviewed_products": top_products.to_dict(orient="records")
            },
            "visualizations": visualizations
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"message": f"File not found: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error processing data: {str(e)}"})


#Opportunitites KPI - 1. High Growth Rate in Adjacent Categories
KPI2_PATH = "SWOTdata/KPI2 - Sheet1.csv"

async def analyze_high_growth_adjacent_categories():
    """
    Endpoint to analyze high growth rate in adjacent market categories.
    """
    try:
        # Load and clean data
        df = pd.read_csv(KPI2_PATH, skiprows=4)
        df = df[['Market Category', 'CAGR (%)', 'Region', 'Relevance to Haldiram’s']]
        df['CAGR (%)'] = df['CAGR (%)'].str.rstrip('%').astype(float)
        df = df.dropna(subset=['CAGR (%)'])

        # Calculate Growth Score with modifiers based on relevance
        def calculate_growth_score(row):
            base_score = row['CAGR (%)']
            relevance = str(row['Relevance to Haldiram’s']).lower()
            if 'expansion' in relevance:
                return base_score * 1.2  # 20% bonus
            elif 'core' in relevance:
                return base_score * 0.8  # 20% reduction
            else:
                return base_score
        
        df['Growth Score'] = df.apply(calculate_growth_score, axis=1)

        # Aggregate to create KPI table
        kpi_table = df.groupby('Market Category').agg({
            'CAGR (%)': 'mean',
            'Growth Score': 'mean',
            'Region': 'first',
            'Relevance to Haldiram’s': 'first'
        }).sort_values('Growth Score', ascending=False)

        # Add Priority Rank
        kpi_table['Priority Rank'] = range(1, len(kpi_table) + 1)

        # Key Takeaways
        key_takeaways = [
            "1. Top Expansion Opportunities:",
            kpi_table[['Growth Score', 'Relevance to Haldiram’s']].head(3).to_markdown(),
            "",
            "2. Regional Focus Recommendations:",
            f"- India shows highest average growth potential ({kpi_table[kpi_table['Region'] == 'India']['Growth Score'].mean():.1f} score)",
            f"- Global markets show steady but lower growth ({kpi_table[kpi_table['Region'] == 'Global']['Growth Score'].mean():.1f} score)",
            "",
            "3. Strategic Recommendations:",
            "- Prioritize frozen foods expansion (highest growth score)",
            "- Leverage ethnic snacks expertise for adjacent product development",
            "- Explore plant-based options despite data limitations (emerging trend)"
        ]

        # Visualizations
        sns.set_theme()
        plt.figure(figsize=(14, 8))

        visualizations = {}

        # Plot 1: Growth Score by Category
        plt.subplot(2, 2, 1)
        sns.barplot(x='Growth Score', y=kpi_table.index, data=kpi_table.reset_index(), palette='viridis')
        plt.title('Growth Potential Score by Market Category')
        plt.xlabel('Growth Score')
        plt.ylabel('')
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight')
        img1.seek(0)
        visualizations["growth_score_bar"] = f"data:image/png;base64,{base64.b64encode(img1.getvalue()).decode()}"
        plt.clf()

        # Plot 2: CAGR Comparison
        plt.subplot(2, 2, 2)
        sns.barplot(x='CAGR (%)', y=kpi_table.index, data=kpi_table.reset_index(), palette='magma')
        plt.title('Raw CAGR by Market Category')
        plt.xlabel('CAGR (%)')
        plt.ylabel('')
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight')
        img2.seek(0)
        visualizations["cagr_bar"] = f"data:image/png;base64,{base64.b64encode(img2.getvalue()).decode()}"
        plt.clf()

        # Plot 3: Region-wise Growth Potential Pie Chart
        plt.subplot(2, 2, 3)
        region_growth = kpi_table.groupby('Region')['Growth Score'].mean().sort_values()
        region_growth.plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
        plt.title('Growth Potential by Region')
        plt.ylabel('')
        img3 = io.BytesIO()
        plt.savefig(img3, format='png', bbox_inches='tight')
        img3.seek(0)
        visualizations["region_growth_pie"] = f"data:image/png;base64,{base64.b64encode(img3.getvalue()).decode()}"
        plt.clf()

        # Plot 4: Priority Ranking Scatter Plot
        plt.subplot(2, 2, 4)
        sns.scatterplot(
            x='CAGR (%)', y='Growth Score', hue=kpi_table.index,
            size='Priority Rank', sizes=(100, 400), data=kpi_table.reset_index()
        )
        plt.title('Growth Potential vs Raw CAGR')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        img4 = io.BytesIO()
        plt.savefig(img4, format='png', bbox_inches='tight')
        img4.seek(0)
        visualizations["growth_vs_cagr_scatter"] = f"data:image/png;base64,{base64.b64encode(img4.getvalue()).decode()}"
        plt.close()

        # Prepare response
        return {
            "analysis_results": {
                "data_table": kpi_table.reset_index().to_dict(orient='records'),
                "formatted_table": kpi_table[['CAGR (%)', 'Growth Score', 'Priority Rank', 'Region', 'Relevance to Haldiram’s']].to_markdown(),
                "key_takeaways": key_takeaways
            },
            "visualizations": visualizations
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"message": f"File not found: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error processing data: {str(e)}"})
    
# Opportunities KPI - 2. Rising Trend Alignment (e.g., Health, Sustainability)
KPI4_PATH = "SWOTdata/KPI - KPI-4.csv"
KPI10_PATH = "SWOTdata/KPI - KPI-10.csv"
KPI11_PATH = "SWOTdata/KPI - KPI-11.csv"
async def analyze_trend_alignment():
    """
    Analyze rising trend alignment based on KPIs 4, 10, and 11.
    Returns data table, key takeaways, and multiple visualizations.
    """
    try:
        # Load and preprocess data
        sns.set_style("whitegrid")
        sns.set_context("notebook", font_scale=1.1)

        # KPI 4 - Search Volume Trends
        search_data = pd.read_csv(KPI4_PATH, skiprows=2)
        search_data['Date'] = pd.to_datetime(search_data['Date'])
        search_data = search_data[['Date', 'Category', 'Relative Interest']]

        # KPI 10 - Sustainability Focus
        sustainability_data = pd.read_csv(KPI10_PATH)
        sustainability_data['Date'] = pd.to_datetime(sustainability_data['Date'])
        sustainability_data = sustainability_data[['Date', 'Keyword Mentioned']].rename(columns={'Keyword Mentioned': 'Keyword'})

        # KPI 11 - Health & Wellness Trends
        health_data = pd.read_csv(KPI11_PATH, skiprows=2)
        health_data['Date'] = pd.to_datetime(health_data['Date'])
        health_data = health_data[['Date', 'Keyword Mentioned']].rename(columns={'Keyword Mentioned': 'Keyword'})

        # Calculate Trend Growth Scores
        def calculate_trend_score(df):
            df['Year'] = df['Date'].dt.year
            yearly_avg = df.groupby(['Category', 'Year'])['Relative Interest'].mean().unstack()
            growth_rates = yearly_avg.pct_change(axis=1) * 100  # YoY growth in %
            return growth_rates.mean(axis=1).fillna(0)  # Average growth rate per category

        search_scores = calculate_trend_score(search_data)

        # Normalize keyword counts for sustainability and health
        sustainability_score = len(sustainability_data) / 10
        health_score = len(health_data) / 10

        # Compose combined trend alignment table
        trend_alignment = pd.DataFrame({
            'Trend Category': ['Healthy Snacks', 'Sustainable Packaging', 'Online Grocery Delivery'],
            'Search Growth (%)': [
                search_scores.get('Healthy Snacks', 0),
                search_scores.get('Sustainable Packaging', 0),
                search_scores.get('Online Grocery Delivery', 0)
            ],
            'Industry Focus': [health_score, sustainability_score, 0],  # Online grocery has no KPI10/11 data
            'Composite Score': [
                0.6 * search_scores.get('Healthy Snacks', 0) + 0.4 * health_score,
                0.6 * search_scores.get('Sustainable Packaging', 0) + 0.4 * sustainability_score,
                1.0 * search_scores.get('Online Grocery Delivery', 0)
            ]
        }).sort_values('Composite Score', ascending=False)

        trend_alignment['Priority'] = range(1, len(trend_alignment) + 1)

        # Visualizations container
        visualizations = {}

        # Plot 1: Composite Scores Barplot
        plt.figure(figsize=(16, 12))
        plt.subplot(2, 2, 1)
        ax1 = sns.barplot(x='Composite Score', y='Trend Category', data=trend_alignment, palette='viridis')
        plt.title('Trend Alignment Composite Scores', pad=20)
        plt.xlabel('Composite Score', labelpad=10)
        plt.ylabel('Trend Category', labelpad=10)
        ax1.grid(True, linestyle='--', alpha=0.6)

        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight')
        img1.seek(0)
        visualizations["composite_scores"] = f"data:image/png;base64,{base64.b64encode(img1.getvalue()).decode()}"
        plt.clf()

        # Plot 2: Score Components Breakdown (stacked bar)
        plt.subplot(2, 2, 2)
        ax2 = trend_alignment.set_index('Trend Category')[['Search Growth (%)', 'Industry Focus']].plot(
            kind='bar', stacked=True, colormap='coolwarm', ax=plt.gca())
        plt.title('Score Components Breakdown', pad=20)
        plt.xlabel('Trend Category', labelpad=10)
        plt.ylabel('Score Value', labelpad=10)
        plt.legend(bbox_to_anchor=(1.02, 1), title='Component')
        ax2.grid(True, linestyle='--', alpha=0.6)

        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight')
        img2.seek(0)
        visualizations["score_components_breakdown"] = f"data:image/png;base64,{base64.b64encode(img2.getvalue()).decode()}"
        plt.clf()

        # Plot 3: Search Trend Evolution (lineplot)
        plt.subplot(2, 2, 3)
        ax3 = sns.lineplot(data=search_data, x='Date', y='Relative Interest', hue='Category',
                           palette='bright', linewidth=2.5)
        plt.title('Search Trend Evolution', pad=20)
        plt.xlabel('Date', labelpad=10)
        plt.ylabel('Relative Interest', labelpad=10)
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.02, 1), title='Category')
        ax3.grid(True, linestyle='--', alpha=0.6)

        img3 = io.BytesIO()
        plt.savefig(img3, format='png', bbox_inches='tight')
        img3.seek(0)
        visualizations["search_trend_evolution"] = f"data:image/png;base64,{base64.b64encode(img3.getvalue()).decode()}"
        plt.clf()

        # Plot 4: Industry Keyword Focus (barplot)
        plt.subplot(2, 2, 4)
        keyword_counts = pd.concat([
            sustainability_data['Keyword'].value_counts(),
            health_data['Keyword'].value_counts()
        ], axis=1).fillna(0)
        keyword_counts.columns = ['Sustainability', 'Health']
        ax4 = keyword_counts.plot(kind='bar', ax=plt.gca(), width=0.8)
        plt.title('Industry Keyword Focus', pad=20)
        plt.xlabel('Keyword', labelpad=10)
        plt.ylabel('Mention Count', labelpad=10)
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.02, 1))
        ax4.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(pad=3.0, w_pad=2.5, h_pad=2.5)

        img4 = io.BytesIO()
        plt.savefig(img4, format='png', bbox_inches='tight')
        img4.seek(0)
        visualizations["industry_keyword_focus"] = f"data:image/png;base64,{base64.b64encode(img4.getvalue()).decode()}"
        plt.close()

        # Key takeaways
        key_takeaways = [
            "1. Top Aligned Trends:",
            trend_alignment.head(2)[['Trend Category', 'Composite Score']].to_markdown(index=False),
            "",
            "2. Strategic Recommendations:",
            "- Capitalize on healthy snacks trend (highest alignment)",
            "- Develop sustainable packaging solutions (growing industry focus)",
            "- Monitor online grocery for potential partnerships",
            "",
            "3. Risk Factors:",
            "- Healthy snacks competition may intensify",
            "- Sustainable packaging requires R&D investment",
            "- Online grocery lacks industry keyword support"
        ]

        # Prepare response
        return {
            "analysis_results": {
                "data_table": trend_alignment.to_dict(orient='records'),
                "formatted_table": trend_alignment.to_markdown(index=False),
                "key_takeaways": key_takeaways,
            },
            "visualizations": visualizations
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"message": f"File not found: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Error processing data: {str(e)}"})

# Opportunities KPI - 3. Unmet Needs Identified in Reviews
KPI78_PATH = "SWOTdata/KPI78.csv"

async def analyze_unmet_needs():
    """
    Endpoint to analyze unmet needs from customer reviews.
    Uses a predefined file path (hardcoded in the application).
    Returns visualizations, analysis results, and recommendations.
    """
    try:
        # Load and process data
        df = pd.read_csv(KPI78_PATH)
        
        # Extract unmet needs
        unmet_needs = []
        for item in df['REVIEWS - UNMET NEEEDS']:
            if isinstance(item, str) and not item.startswith('"""') and not item.startswith('Delicious'):
                clean_item = re.sub(r'^- ', '', item.strip())
                if clean_item:
                    unmet_needs.append(clean_item)

        # Define categories
        categories = {
            'Packaging': ['resealable', 'zip-lock', 'packaging', 'freshness'],
            'Healthier Options': ['baked', 'sugar-free', 'lower fat', 'healthier', 'calorie', 'less oily'],
            'Flavor Profile': ['citric acid', 'tangy', 'milder', 'spice level', 'saltiness', 'balanced', 'sweetness'],
            'Availability': ['availability', 'town', 'city', 'accessible'],
            'Pricing': ['affordable', 'pricing', 'price', 'expensive'],
            'Ingredients': ['additives', 'palm oil', 'artificial'],
            'Variety': ['variety', 'regional', 'specialty', 'flavors']
        }

        # Categorize needs
        def categorize_needs(text):
            text_lower = text.lower()
            for category, keywords in categories.items():
                if any(keyword in text_lower for keyword in keywords):
                    return category
            return 'Other'

        feedback_df = pd.DataFrame(unmet_needs, columns=['Raw Feedback'])
        feedback_df['Category'] = feedback_df['Raw Feedback'].apply(categorize_needs)
        category_counts = feedback_df['Category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']

        # Calculate priority scores
        priority_weights = {
            'Healthier Options': 1.2,
            'Packaging': 1.1,
            'Flavor Profile': 1.0,
            'Pricing': 0.9,
            'Availability': 0.8,
            'Variety': 0.7,
            'Ingredients': 0.6,
            'Other': 0.5
        }

        category_counts['Priority Score'] = category_counts.apply(
            lambda x: x['Count'] * priority_weights[x['Category']], axis=1)
        category_counts = category_counts.sort_values('Priority Score', ascending=False)

        # Create KPI table with actions
        action_map = {
            'Packaging': 'Develop resealable/zip-lock packaging',
            'Healthier Options': 'Expand baked/sugar-free product lines',
            'Flavor Profile': 'Reformulate flavor profiles based on feedback',
            'Pricing': 'Review pricing strategy for key products',
            'Availability': 'Improve distribution network',
            'Variety': 'Introduce regional specialty variants',
            'Ingredients': 'Reduce artificial additives',
            'Other': 'Investigate and address miscellaneous concerns'
        }
        kpi_table = category_counts.copy()
        kpi_table['Action Recommended'] = kpi_table['Category'].map(action_map).fillna('Investigate further')

        # Generate visualizations
        sns.set_theme()
        visualizations = {}

        # Plot 1: Unmet Needs by Category
        plt.figure(figsize=(12, 6))
        ax1 = sns.barplot(x='Count', y='Category', data=category_counts, palette='viridis')
        plt.title('Unmet Needs by Category', pad=15)
        plt.xlabel('Number of Mentions', labelpad=10)
        plt.ylabel('Category', labelpad=10)
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight')
        img1.seek(0)
        visualizations["needs_by_category"] = f"data:image/png;base64,{base64.b64encode(img1.getvalue()).decode('utf-8')}"
        plt.close()

        # Plot 2: Priority Scores
        plt.figure(figsize=(12, 6))
        ax2 = sns.barplot(x='Priority Score', y='Category', data=category_counts, palette='magma')
        plt.title('Priority Scores by Category', pad=15)
        plt.xlabel('Priority Score', labelpad=10)
        plt.ylabel('Category', labelpad=10)
        ax2.grid(True, linestyle='--', alpha=0.6)
        
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight')
        img2.seek(0)
        visualizations["priority_scores"] = f"data:image/png;base64,{base64.b64encode(img2.getvalue()).decode('utf-8')}"
        plt.close()

        # Plot 3: Word Cloud
        plt.figure(figsize=(12, 6))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(unmet_needs))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Common Themes in Feedback', pad=15)
        
        img3 = io.BytesIO()
        plt.savefig(img3, format='png', bbox_inches='tight')
        img3.seek(0)
        visualizations["word_cloud"] = f"data:image/png;base64,{base64.b64encode(img3.getvalue()).decode('utf-8')}"
        plt.close()

        # Plot 4: Top Needs Distribution
        plt.figure(figsize=(8, 8))
        top_needs = feedback_df['Category'].value_counts().nlargest(3).index
        trend_data = feedback_df[feedback_df['Category'].isin(top_needs)]['Category'].value_counts()
        ax4 = trend_data.plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
        plt.title('Top 3 Unmet Needs Distribution', pad=15)
        plt.ylabel('')
        
        img4 = io.BytesIO()
        plt.savefig(img4, format='png', bbox_inches='tight')
        img4.seek(0)
        visualizations["top_needs_distribution"] = f"data:image/png;base64,{base64.b64encode(img4.getvalue()).decode('utf-8')}"
        plt.close()

        # Prepare key takeaways
        key_takeaways = {
            "top_priority_needs": kpi_table.head(3)[['Category', 'Count', 'Priority Score']].to_dict(orient='records'),
            "strategic_recommendations": [
                "Immediately address packaging improvements (highest frequency)",
                "Develop 2-3 healthier product variants within 6 months",
                "Conduct flavor profile testing with consumer panels"
            ],
            "quick_wins": [
                "Introduce resealable packaging for top 3 products",
                "Create 'milder flavor' versions of spicy products",
                "Launch pilot program for regional specialties"
            ],
            "long_term_opportunities": [
                "R&D investment in sugar-free formulations",
                "Supply chain optimization for better availability",
                "Clean-label ingredient initiatives"
            ]
        }

        # Prepare response
        return {
            "analysis_results": {
                "kpi_table": kpi_table.to_dict(orient='records'),
                "formatted_kpi_table": kpi_table.to_markdown(index=False),
                "raw_feedback_samples": unmet_needs[:10]  # Sample of raw feedback
            },
            "visualizations": visualizations,
            "key_takeaways": key_takeaways
        }

    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"message": f"File not found at path: {KPI78_PATH}. Please check the file path in the application code."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing data: {str(e)}"}
        )
# Opportunities KPI - 4. Competitor Weaknesses Identified
FILE_PATH = "SWOTdata/KPI40 - KPI40.csv"

async def analyze_competitor_weaknesses():
    """
    Endpoint to analyze competitor weaknesses and identify opportunities.
    Uses a predefined file path (hardcoded in the application).
    Returns visualizations, analysis results, and strategic recommendations.
    """
    try:
        # Load and transform data
        df = pd.read_csv(FILE_PATH)
        competitor_data = {}
        for column in df.columns:
            competitor_data[column] = df[column].dropna().tolist()

        # Categorize weaknesses
        weakness_categories = {
            'Quality Control': ['inconsistent', 'quality', 'freshness', 'contamination', 'hygiene'],
            'Pricing': ['pricing', 'price', 'high', 'expensive'],
            'Distribution': ['distribution', 'channels', 'network', 'gaps', 'regions'],
            'Brand Perception': ['awareness', 'image', 'traditional', 'regional'],
            'Product Portfolio': ['variety', 'portfolio', 'limited'],
            'Operations': ['sourcing', 'financial', 'costs', 'incident']
        }

        # Create analysis dataframe
        analysis = []
        for competitor, weaknesses in competitor_data.items():
            for weakness in weaknesses:
                analysis.append({'Competitor': competitor, 'Weakness': weakness})

        df_analysis = pd.DataFrame(analysis)

        # Categorize each weakness
        def categorize_weakness(text):
            text_lower = text.lower()
            for category, keywords in weakness_categories.items():
                if any(keyword in text_lower for keyword in keywords):
                    return category
            return 'Other'

        df_analysis['Category'] = df_analysis['Weakness'].apply(categorize_weakness)

        # Calculate opportunity scores
        opportunity_weights = {
            'Quality Control': 1.3,
            'Pricing': 1.1,
            'Distribution': 1.2,
            'Brand Perception': 1.0,
            'Product Portfolio': 0.9,
            'Operations': 0.8,
            'Other': 0.5
        }

        # Count weaknesses by category and competitor
        category_counts = df_analysis.groupby(['Competitor', 'Category']).size().unstack().fillna(0)
        category_scores = category_counts * pd.Series(opportunity_weights)

        # Calculate total opportunity score per competitor
        category_scores['Total Opportunity'] = category_scores.sum(axis=1)
        category_scores = category_scores.sort_values('Total Opportunity', ascending=False)

        # Calculate Haldiram's relative position
        haldiram_weaknesses = df_analysis[df_analysis['Competitor'] == "Haldiram's"]['Category'].value_counts()
        competitor_weaknesses = df_analysis[df_analysis['Competitor'] != "Haldiram's"]

        # Generate visualizations
        visualizations = {}
        plt.figure(figsize=(18, 12))
        plt.suptitle('Competitor Weakness Analysis', y=1.02, fontsize=16)

        # Plot 1: Competitor Weakness Heatmap
        plt.subplot(2, 2, 1)
        if not category_counts.empty:
            sns.heatmap(category_counts, annot=True, cmap='YlOrRd', fmt='g')
            plt.title('Competitor Weaknesses by Category', pad=12)
            plt.ylabel('Competitor', labelpad=10)
            plt.xlabel('Weakness Category', labelpad=10)
        else:
            plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
            plt.title('No Data Available', pad=12)
        
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight')
        img1.seek(0)
        visualizations["weakness_heatmap"] = f"data:image/png;base64,{base64.b64encode(img1.getvalue()).decode('utf-8')}"
        plt.clf()

        # Plot 2: Opportunity Scores
        plt.subplot(2, 2, 2)
        if not category_scores.empty:
            category_scores.drop('Total Opportunity', axis=1).plot(
                kind='bar', stacked=True, colormap='viridis', ax=plt.gca())
            plt.title('Weighted Opportunity Scores by Competitor', pad=12)
            plt.ylabel('Opportunity Score', labelpad=10)
            plt.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        else:
            plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
            plt.title('No Data Available', pad=12)
        
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight')
        img2.seek(0)
        visualizations["opportunity_scores"] = f"data:image/png;base64,{base64.b64encode(img2.getvalue()).decode('utf-8')}"
        plt.clf()

        # Plot 3: Haldiram's vs Competitors
        plt.subplot(2, 2, 3)
        if not competitor_weaknesses.empty and not haldiram_weaknesses.empty:
            comp_weakness_counts = competitor_weaknesses['Category'].value_counts()
            (comp_weakness_counts - haldiram_weaknesses).fillna(comp_weakness_counts).plot(
                kind='bar', color='green')
            plt.title("Haldiram's Competitive Advantages", pad=12)
            plt.ylabel('Weakness Count Difference', labelpad=10)
            plt.axhline(0, color='black', linestyle='--')
        else:
            plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
            plt.title('No Data Available', pad=12)
        
        img3 = io.BytesIO()
        plt.savefig(img3, format='png', bbox_inches='tight')
        img3.seek(0)
        visualizations["competitive_advantages"] = f"data:image/png;base64,{base64.b64encode(img3.getvalue()).decode('utf-8')}"
        plt.clf()

        # Plot 4: Top Weaknesses to Exploit
        plt.subplot(2, 2, 4)
        if not competitor_weaknesses.empty:
            top_weaknesses = competitor_weaknesses['Weakness'].value_counts().nlargest(5)
            if not top_weaknesses.empty:
                top_weaknesses.plot(kind='barh', color='purple')
                plt.title('Top 5 Competitor Weaknesses', pad=12)
                plt.xlabel('Number of Mentions', labelpad=10)
            else:
                plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
                plt.title('No Data Available', pad=12)
        else:
            plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
            plt.title('No Data Available', pad=12)
        
        img4 = io.BytesIO()
        plt.savefig(img4, format='png', bbox_inches='tight')
        img4.seek(0)
        visualizations["top_weaknesses"] = f"data:image/png;base64,{base64.b64encode(img4.getvalue()).decode('utf-8')}"
        plt.close()

        # Create KPI Table and recommendations
        if not category_scores.empty:
            kpi_table = pd.DataFrame({

                'Competitor': category_scores.index,
                'Total Opportunity Score': category_scores['Total Opportunity'],
                'Primary Weaknesses': category_scores.idxmax(axis=1),
                'Recommended Focus Areas': [
                    "Quality consistency & distribution",
                    "Product variety & pricing",
                    "Modern branding & online presence",
                    "Quality assurance & distribution",
                    "Brand building & product expansion"
                ]
            })

            # Prepare key takeaways
            key_takeaways = {
                "top_opportunities": kpi_table.head(3).to_dict(orient='records'),
                "strategic_recommendations": [
                    "Launch quality assurance marketing campaign highlighting Haldiram's standards",
                    "Introduce competitive pricing for key products where competitors are weak",
                    "Expand distribution in regions where competitors have gaps"
                ],
                "competitive_advantages": [
                    "Fewer quality control issues than Gopal Snacks (exploit in marketing)",
                    "Stronger brand awareness than Prataap Snacks",
                    "More national presence than Bikanervala"
                ],
                "action_plan": [
                    {"timeline": "Short-term", "action": "Highlight quality differentiators in advertising"},
                    {"timeline": "Mid-term", "action": "Address pricing perception through value packs"},
                    {"timeline": "Long-term", "action": "Expand distribution to under-served areas"}
                ]
            }

            # Prepare response
            return {
                "analysis_results": {
                    "kpi_table": kpi_table.to_dict(orient='records'),
                    "formatted_kpi_table": kpi_table.to_markdown(index=False),
                    "category_breakdown": category_counts.reset_index().to_dict(orient='records')
                },
                "visualizations": visualizations,
                "key_takeaways": key_takeaways
            }
        else:
            return JSONResponse(
                status_code=404,
                content={"message": "No data available for analysis"}
            )

    except FileNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"message": f"File not found at path: {FILE_PATH}. Please check the file path in the application code."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing data: {str(e)}"}
        )

# Opportunities KPI - 5. Untapped Geographic Search Interest
def geographic_search_opportunity():
    try:
        kpi13_path = 'SWOTdata/KPI13 - KPI-13.csv'
        kpi71_path = 'SWOTdata/KPI 71 - Sheet1.csv'

        # Load data
        kpi13 = pd.read_csv(kpi13_path)
        kpi71 = pd.read_csv(kpi71_path)

        # Prepare KPI 13 data
        geo_data = kpi13[['Region/City', 'Search Term', 'Relative Search Interest (0-100)']].copy()
        geo_data.columns = ['Region/City', 'Search Term', 'Relative Search Interest']

        # Prepare KPI 71 data
        penetration_data = kpi71[['Region', 'Haldiram: (India)']].dropna().copy()
        penetration_data.columns = ['Region/City', 'Current Penetration (%)']
        penetration_data['Current Penetration (%)'] = penetration_data['Current Penetration (%)'].str.rstrip('%').astype(float)

        # Merge and filter
        merged = pd.merge(
            geo_data[geo_data['Search Term'].str.lower() == 'buy namkeen online'],
            penetration_data,
            on='Region/City',
            how='inner'
        )

        # Compute Opportunity Score
        merged['Opportunity Score'] = (
            (merged['Relative Search Interest'] * 0.7) +
            ((100 - merged['Current Penetration (%)']) * 0.3)
        )

        # Classify region
        merged['Region Type'] = np.where(
            merged['Region/City'].isin(['Delhi', 'Mumbai', 'Bangalore', 'Kolkata']),
            'Tier 1 India',
            np.where(
                merged['Region/City'].isin(['Hyderabad', 'Chennai', 'Pune', 'Ahmedabad']),
                'Tier 2 India',
                'International'
            )
        )

        # Final KPI Table
        merged = merged.sort_values('Opportunity Score', ascending=False).reset_index(drop=True)
        merged['Priority'] = merged.index + 1

        kpi_table = merged[['Region/City', 'Region Type', 'Relative Search Interest',
                            'Current Penetration (%)', 'Opportunity Score', 'Priority']]

        return {
            "status": "success",
            "kpi": "Geographic Opportunity Analysis (KPI-13 & KPI-71)",
            "insights": {
                "top_5_opportunity_markets": kpi_table.head(5)[['Region/City', 'Opportunity Score']].to_dict(orient='records'),
                "strategic_recommendations": [
                    "Focus marketing on high-opportunity markets with localized campaigns",
                    "Expand distribution through retail partnerships in Tier 2 cities",
                    "Develop e-commerce push for international markets with delivery guarantees"
                ],
                "quick_wins": [
                    "Boost digital ads in high-search, low-penetration markets",
                    "Create region-specific product bundles for emerging markets"
                ],
                "long_term_opportunities": [
                    "Establish local partnerships in Middle Eastern markets",
                    "Develop export-optimized packaging for Western markets",
                    "Implement geo-targeted social media campaigns"
                ]
            },
            "table": kpi_table.to_dict(orient='records'),
            "meta": {
                "total_markets_evaluated": len(kpi_table),
                "date_generated": datetime.now().strftime("%Y-%m-%d")
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


