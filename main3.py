# section E : Swot analysis
from fastapi import FastAPI
from typing import Dict, Any
from SWOTkpi.Source import (
    analyze_review_themes as analyze_review_themes_logic,
    analyze_social_media_metrics as analyze_social_media_metrics_logic,
    analyze_website_issues as analyze_website_issues_logic,
    analyze_response_rates as analyze_response_rates_logic,
    news_sentiment_spikes as news_sentiment_spikes_logic,
    search_volume_rank as search_volume_rank_logic,
    analyze_sentiment_score as analyze_sentiment_score_logic,
    product_range_visibility as product_range_visibility_logic,
    analyze_ecommerce_presence as analyze_ecommerce_presence_logic,
    high_review_volume as high_review_volume_logic,
    analyze_high_growth_adjacent_categories as analyze_high_growth_adjacent_categories_logic,
    analyze_trend_alignment as analyze_trend_alignment_logic,
    analyze_unmet_needs as analyze_unmet_needs_logic,
    analyze_competitor_weaknesses as analyze_competitor_weaknesses_logic,
    geographic_search_opportunity as geographic_search_opportunity_logic,
)

app = FastAPI(title="SWOT Specific Indicators APIs")

@app.get("/E1_Strength/High_Brand_Search_Volume_Rank/")
async def search_volume_rank() -> Dict[str, Any]:
    return await search_volume_rank_logic()

@app.get("/E2_Strength/Positive_Overall_Sentiment_Score/")
async def analyze_sentiment_score() -> Dict[str, Any]:
    return await analyze_sentiment_score_logic()

@app.get("/E3_Strength/Wide_Product_Range_Visibility/")
async def product_range_visibility() -> Dict[str, Any]:
    return await product_range_visibility_logic()

@app.get("/E4_Strength/Strong_Ecommerce_Presence/Ratings/")
async def analyze_ecommerce_presence() -> Dict[str, Any]:
    return await analyze_ecommerce_presence_logic()

@app.get("/E5_Strength/High_review_volume/")
async def high_review_volume() -> Dict[str, Any]:
    return await high_review_volume_logic()

@app.get("/E6_Weakness/Key_Negative_Review_Themes_Frequency")
def analyze_review_themes() -> Dict[str, Any]:
    return analyze_review_themes_logic()

@app.get("/E7_Weakness/Lower_Engagement_Rate_vs_Select_Competitors/")
def analyze_social_media_metrics() -> Dict[str, Any]:
    return analyze_social_media_metrics_logic()

@app.get("/E8_Weakness/Identified_Website_usability_issues/")
def analyze_website_issues() -> Dict[str, Any]:
    return analyze_website_issues_logic()

@app.get("/E9_Weakness/Gaps_in_Online_Customer_Service_Response/")
async def analyze_response_rates() -> Dict[str, Any]:
    return await analyze_response_rates_logic()

@app.get("/E10_Weakness/Negative_News_Sentiment_Spikes/")
async def news_sentiment_spikes() -> Dict[str, Any]:
    return await news_sentiment_spikes_logic()

@app.get("/E11_Opportunities/High_Growth_Rate_In_Adjacent_Categories/")
async def analyze_high_growth_adjacent_categories() -> Dict[str, Any]:
    return await analyze_high_growth_adjacent_categories_logic()

@app.get("/E12_Opportunities/Rising_Trend_Alignment/")
async def analyze_trend_alignment() -> Dict[str, Any]:
    return await analyze_trend_alignment_logic()

@app.get("/E13_Opportunities/Unmet_Needs_Identified_In_Reviews/")
async def analyze_unmet_needs() -> Dict[str, Any]:
    return await analyze_unmet_needs_logic()

@app.get("/E14_Opportunities/Competitor_Weaknesses_Identified/")
async def analyze_competitor_weaknesses() -> Dict[str, Any]:
    return await analyze_competitor_weaknesses_logic()

@app.get("/E15_Opportunities/Untapped_Geographic_Search_Interest/")
def geographic_search_opportunity() -> Dict[str, Any]:
    return  geographic_search_opportunity_logic()

# Competitive and advanced competitive analysis endpoints
from fastapi.responses import StreamingResponse, Response
from adv_comp.backlink import backlink_endpoint
from adv_comp.Content_Marketing_Sophistication import content_marketing_endpoint
from adv_comp.emp_rating import emp_rating_endpoint
from adv_comp.geo_expan import geo_expansion_endpoint
from adv_comp.innovation_rate import innovation_rate_endpoint
import io
from adv_comp.leadership_visibility import leadership_visibility_endpoint
from adv_comp.LitigationRegulatory import litigation_issue_data, litigation_issue_plot
from fastapi.responses import StreamingResponse
from adv_comp.marketing_msg_consistency import marketing_message_scores, marketing_message_consistency_plot
import io
from adv_comp.narrative_control import narrative_control_data, narrative_control_plot
from adv_comp.niche_targeting import niche_targeting_plot
from adv_comp.patnership_network import get_partnership_data
from adv_comp.pivot import get_strategic_pivot_dossier
from adv_comp.pricing_strat_agg import get_pricing_aggressiveness_table, get_pricing_aggressiveness_plot
from adv_comp.product_issue import analyze_product_issues
from adv_comp.response import load_competitor_responses
from adv_comp.social_listening_eng import load_and_process_engagement
from adv_comp.talent import load_talent_acquisition_data
from adv_comp.tech import load_tech_adoption_summary
from adv_comp.vulnerability import load_and_rank_competitors
from fastapi.responses import JSONResponse
from adv_comp.backlink import process_backlink_data

#adv_comp endpoints
@app.get("/G-7/backlink-quality")
def get_backlink_quality():
    csv_path = "data/Competitor Website Backlink Qua.csv"
    result_df = process_backlink_data(csv_path)
    return JSONResponse(content=result_df.to_dict(orient="records"))

@app.get("/G-14/content-marketing-sophistication")
def get_content_marketing_sophistication():
    return content_marketing_endpoint()

@app.get("/G-11/emp-rating")
async def get_emp_rating():
    return await emp_rating_endpoint()

@app.get("/G-9/geo-expansion")
def get_geo_expansion():
    img_bytes = geo_expansion_endpoint()
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

@app.get("/G-4/innovation-rate")
def get_innovation_rate():
    return innovation_rate_endpoint()

@app.get("/G-16/leadership-visibility")
def get_leadership_visibility():
    return leadership_visibility_endpoint()

@app.get("/G-17/litigation-issues/plot")
def get_litigation_issues_plot():
    image_bytes = litigation_issue_plot()
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")

@app.get("/G-2/marketing-message-scores")
def get_marketing_scores():
    return marketing_message_scores()

@app.get("/G-2/marketing-message-consistency-plot")
def get_marketing_plot():
    img_bytes = marketing_message_consistency_plot()
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")
@app.get("/G-10/narrative-control-data")
def get_narrative_control_data():
    return narrative_control_data()

@app.get("/G-10/narrative-control-plot")
def get_narrative_control_plot():
    img_bytes = narrative_control_plot()
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

@app.get("/G-24/niche-targeting-plot")
def get_niche_targeting_plot():
    img_bytes = niche_targeting_plot()
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")
@app.get("/G-5/partnership-network")
def partnership_network():
    data = get_partnership_data()
    return {"partnerships": data}
@app.get("/G-1/strategic-pivot-dossier")
def strategic_pivot_dossier():
    data = get_strategic_pivot_dossier()
    return {"dossiers": data}

@app.get("/G-8/pricing-aggressiveness-table")
def pricing_aggressiveness_table():
    data = get_pricing_aggressiveness_table()
    return {"pricing_aggressiveness": data}

@app.get("/G-8/pricing-aggressiveness-plot")
def pricing_aggressiveness_plot():
    img_bytes = get_pricing_aggressiveness_plot()
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

from fastapi.responses import StreamingResponse, JSONResponse
from adv_comp.product_issue import analyze_product_issues, get_product_issue_chart

@app.get("/G-23/product-issue-analysis")
def run_product_issue_analysis():
    results = analyze_product_issues()
    return JSONResponse(content=results)

@app.get("/G-23/product-issue-chart")
def product_issue_chart():
    img_buf = get_product_issue_chart()
    return StreamingResponse(img_buf, media_type="image/png")
@app.get("/G-25/competitor-responses")
def get_competitor_responses():
    data = load_competitor_responses()
    return data
@app.get("/G-15/social-listening-engagement")
def social_listening_engagement():
    data = load_and_process_engagement()
    return {"engagement_data": data}

@app.get("/G-3/talent-acquisition")
def get_talent_acquisition():
    data = load_talent_acquisition_data()
    return {"talent_acquisition": data}

@app.get("/G-12/tech-adoption")
def get_tech_adoption():
    data = load_tech_adoption_summary()
    return {"tech_adoption": data}

@app.get("/G-13/vulnerability/ranks")
def get_competitor_ranks():
    ranked_competitors = load_and_rank_competitors()
    return {"competitor_ranks": ranked_competitors}

#comp endpoints
from fastapi.responses import StreamingResponse
from comp.bounce_rate import generate_bounce_rate_plot

@app.get("/B-1/comp/direct-competitor-kpi")
def direct_competitor_kpi():
    return get_direct_competitor_kpi()

from comp.indirect_competitors_kpi import get_indirect_competitor_kpi

@app.get("/B-2/comp/indirect-competitor-kpi")
def indirect_competitor_kpi():
    return get_indirect_competitor_kpi()
from comp.profile_completeness import get_profile_completeness

@app.get("/B-3/comp/profile-completeness")
def profile_completeness():
    return get_profile_completeness()

from comp.geographic_focus import get_geographic_focus

@app.get("/B-4/comp/geographic-focus")
def geographic_focus():
    return get_geographic_focus()

@app.get("/B-5/comp/CATEGORYbreadth")
def breadth_plot():
    img = generate_breadth_plot()
    return StreamingResponse(img, media_type="image/png")
from comp.direct_competitor_kpi import get_direct_competitor_kpi

from comp.range_depth import generate_range_depth_plot

@app.get("/B-6/comp/range-depth")
def range_depth_plot():
    img = generate_range_depth_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.pricing_tier import get_pricing_tiers

@app.get("/B-7/comp/pricing-tiers")
def pricing_tiers():
    return get_pricing_tiers()

from comp.storefront import get_storefront_data

@app.get("/B-8/comp/storefront")
def storefront():
    return get_storefront_data()
from comp.major_online import generate_major_online_heatmap

@app.get("/B-9/comp/major-online-heatmap")
def major_online_heatmap():
    img = generate_major_online_heatmap()
    return StreamingResponse(img, media_type="image/png")
from comp.social_media import get_social_media_presence

@app.get("/B-10/comp/social-media")
def social_media():
    return get_social_media_presence()

from comp.followers import generate_followers_plot

@app.get("/B-11/comp/followers")
def followers_plot():
    img = generate_followers_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.posting import generate_posting_plot

@app.get("/B-12/comp/posting")
def posting_plot():
    img = generate_posting_plot()
    return StreamingResponse(img, media_type="image/png")
from comp.engagement import generate_engagement_plot

@app.get("/B-13/comp/engagement")
def engagement_plot():
    img = generate_engagement_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.traffic import generate_traffic_plot

@app.get("/B-14/comp/WEBSITEtraffic")
def traffic_plot():
    img = generate_traffic_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.bounce_rate import generate_bounce_rate_plot

@app.get("/B-15/comp/bounce-rate/plot")
def bounce_rate_plot():
    img = generate_bounce_rate_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.breadth import generate_breadth_plot

from comp.SEO_DA import generate_seo_da_plot

@app.get("/B-16/comp/seo-DA")
def seo_da_plot():
    img = generate_seo_da_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.SEO_PA import generate_seo_pa_plot

@app.get("/B-16/comp/seo-PA")
def seo_pa_plot():
    img = generate_seo_pa_plot()
    return StreamingResponse(img, media_type="image/png")
from comp.news import generate_news_mentions_plot

@app.get("/B-17/comp/news")
def news_mentions_plot():
    img = generate_news_mentions_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.sentiment_news import generate_sentiment_pie_chart

@app.get("/B-18/comp/sentiment-news")
def sentiment_news_plot(brand: str = None):
    img = generate_sentiment_pie_chart(brand)
    return StreamingResponse(img, media_type="image/png")
from comp.sent_news2 import generate_sent_news2_plot

@app.get("/B-18/comp/sent-news2")
def sent_news2_plot():
    img = generate_sent_news2_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.marketing_campains import get_marketing_campaigns

@app.get("/B-19/comp/marketing-campaigns")
def marketing_campaigns():
    return get_marketing_campaigns()

from comp.influencer import get_influencer_summary

@app.get("/B-20/comp/influencer")
def influencer_summary():
    return get_influencer_summary()

from comp.stated_value import get_stated_value_propositions

@app.get("/B-21/comp/stated-value")
def stated_value():
    return get_stated_value_propositions()

from comp.new_product import generate_new_product_plot

@app.get("/B-22/comp/new-product")
def new_product_plot():
    img = generate_new_product_plot()
    return StreamingResponse(img, media_type="image/png")

from comp.weakness import get_weaknesses_summary

@app.get("/B-25/comp/weakness")
def weakness_summary():
    return get_weaknesses_summary()

# Section C : Haldiram Brand Perception & Online Presence
from SectionC.kpi1 import generate_search_volume_plot
from SectionC.kpi2 import generate_share_of_search_plot
from SectionC.kpi3 import generate_share_of_search_pie
from SectionC.kpi4 import generate_mention_volume_plot
from SectionC.kpi5 import generate_kpi5_plot
from SectionC.kpi6 import generate_kpi6_pie
from SectionC.kpi7 import generate_follower_count_table
from SectionC.kpi8 import generate_follower_growth_rate_plot
from SectionC.kpi9 import generate_posting_frequency_table
from SectionC.kpi10 import generate_engagement_rate_plot
from SectionC.kpi11 import generate_content_themes_plot
from SectionC.kpi12 import generate_traffic_estimate_table
from SectionC.kpi13 import generate_bounce_rate_table
from SectionC.kpi14 import generate_avg_visit_duration_table
from SectionC.kpi15 import generate_traffic_sources_pie
from SectionC.kpi16 import generate_seo_performance_plot
from SectionC.kpi17 import get_top_organic_keywords
from SectionC.kpi19 import generate_page_speed_table
from SectionC.kpi20 import generate_news_mention_frequency_plot
from SectionC.kpi22 import generate_total_reviews_table
from SectionC.kpi23 import generate_platform_ratings_bar
from SectionC.kpi24 import generate_positive_reviews_bar
from SectionC.kpi25 import generate_negative_reviews_bar
from SectionC.kpi26 import generate_response_rate_table
from SectionC.kpi28 import generate_comparison_table
from SectionC.kpi30 import generate_restaurant_presence_table
from SectionC.kpi29 import generate_qualitative_product_visibility_table
from SectionC.kpi21 import generate_news_sentiment_pie


@app.get("/C1-Haldiram Brand Search Volume Trend")
def get_search_volume_plot():
    img_bytes = generate_search_volume_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C2-Haldiram vs. Competitor Search Volume Trend")
def get_share_of_search_plot():
    img_bytes = generate_share_of_search_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C3-Haldiram Share of Search")
def get_share_of_search_pie():
    img_bytes = generate_share_of_search_pie()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C4-Haldiram Social Media Mention Volume")
def get_mention_volume_plot():
    img_bytes = generate_mention_volume_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C5-Haldiram Social Media Sentiment Score")
def get_kpi5_plot():
    img_bytes = generate_kpi5_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C6-Haldiram Social Media Share of Voice ")
def get_kpi6_pie():
    img_bytes = generate_kpi6_pie()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C7-Haldiram Primary Social Platform Follower Count")
def get_follower_count_table():
    img_bytes = generate_follower_count_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C8-Haldiram Primary Social Platform Follower Growth Rate")
def get_follower_growth_rate_plot():
    img_bytes = generate_follower_growth_rate_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C9-Haldiram Social Media Posting Frequency")
def get_posting_frequency_table():
    img_bytes = generate_posting_frequency_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C10-Haldiram Social Media Engagement Rate")
def get_engagement_rate_plot():
    img_bytes = generate_engagement_rate_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C11-Haldiram Top Performing Social Media Content Themes")
def get_content_themes_plot():
    img_bytes = generate_content_themes_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C12-Haldiram Website Traffic Estimate Rank")
def get_traffic_estimate_table():
    img_bytes = generate_traffic_estimate_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C13-Haldiram Estimated Website Bounce Rate")
def get_bounce_rate_table():
    img_bytes = generate_bounce_rate_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C14-Haldiram Estimated Website Avg. Visit Duration")
def get_avg_visit_duration_table():
    img_bytes = generate_avg_visit_duration_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C15-Haldiram Website Top Traffic Sources")
def get_traffic_sources_pie():
    img_bytes = generate_traffic_sources_pie()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C16-Haldiram Website SEO Performance Indicator")
def get_seo_performance_plot():
    img_bytes = generate_seo_performance_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C17-Haldiram Top Organic Keywords Visibility")
def top_organic_keywords():
    return get_top_organic_keywords()

@app.get("/C19-Haldiram Website Page Load Speed Score")
def get_page_speed_table():
    img_bytes = generate_page_speed_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C20-Haldiram News Mention Frequency")
def get_news_mention_frequency_plot():
    img_bytes = generate_news_mention_frequency_plot()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C21-Haldiram News Sentiment")
def get_news_sentiment_pie():
    img_bytes = generate_news_sentiment_pie()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C22-Haldiram Online Review Volume")
def get_total_reviews_table():
    img_bytes = generate_total_reviews_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C23-Haldiram Average Online Rating")
def get_platform_ratings_bar():
    img_bytes = generate_platform_ratings_bar()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C24-Haldiram Positive Review Themes")
def get_positive_reviews_bar():
    img_bytes = generate_positive_reviews_bar()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C25-Haldiram Negative Review Themes")
def get_negative_reviews_bar():
    img_bytes = generate_negative_reviews_bar()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C26-Haldiram Online Customer Service Response Rate")
def get_response_rate_table():
    img_bytes = generate_response_rate_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C28-Haldiram E-commerce Product Page Quality Score")
def get_comparison_table():
    img_bytes = generate_comparison_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C29-Haldiram New Product Launch Visibility")
def qualitative_product_visibility_table():
    img_bytes = generate_qualitative_product_visibility_table()
    return Response(content=img_bytes, media_type="image/png")

@app.get("/C30-Haldiram Restaurant Presence & Ratings")
def get_restaurant_presence_table():
    img_bytes = generate_restaurant_presence_table()
    return Response(content=img_bytes, media_type="image/png")

# Section I : Advanced Consumer Behavior & Journey Insights (OSINT) 
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from services.basket_composition_service import get_basket_composition_chart
from services.Influence_Attribution import generate_mentions_by_platform_image
from services.Trust_Analysis import generate_trust_analysis_plot
from services.Search_Behaviour_Evolution import generate_search_behavior_evolution_chart
from services.Community_Engagement import community_engagement_chart
from services.User_Segmentation_Proxy import user_segmentation_proxy
from services.Post_Purchase_Dissonance import get_post_purchase_dissonance_chart
from services.Subscription_Intrest_Level import generate_subscription_pie_chart
from services.Mobile_vs_Desktop_interaction import generate_mobile_desktop_bar_chart
from services.Keyword_performancce import generate_high_intent_keyword_trend_chart
from services.Brand_switching import generate_switch_trigger_chart
from services.Platform_role import get_platform_funnel_kpi_chart
from services.Purchase_frequency import generate_purchase_frequency_chart
from services.Return_refund_issue import generate_issue_type_chart
from services.Generation_wise_usage import generate_cross_generation_chart
from services.health_awareness_spectrum import get_health_awareness_chart
from services.Recipe_Integration import get_recipe_usage_figure_bytes
from services.Homemade_vs_local import create_chart_image
from services.Impulse_purchase import generate_impulse_kpi_chart
from services.Unboxing_review import get_unboxing_sentiment_chart
from services.Digital_Payment import generate_payment_issues_chart
from services.Gift_card_mention import create_user_type_pie_chart 
from services.food_hack import generate_hacktype_bar_chart
from services.cultural_discussion import generate_contextual_indicators_chart
from services.Variety_information import generate_information_overload_chart
from services.online_influence import generate_influence_chart
from services.Price_increase_reactions import load_reactions, create_pie_chart

@app.get("/I10/basket-composition", response_class=StreamingResponse)
def basket_chart():
    return get_basket_composition_chart()

@app.get("/I-11_Influence-Attribution-Guesses")
def influence_platform_mentions():
    img_buf = generate_mentions_by_platform_image()
    return StreamingResponse(img_buf, media_type="image/png")

@app.get("/I28/search-behavior", response_class=StreamingResponse)
def search_behavior_chart():
    return generate_search_behavior_evolution_chart()

@app.get("/I27/trust-analysis", response_class=StreamingResponse)
def trust_analysis_chart():
    return generate_trust_analysis_plot()

@app.get("/I26/post-purchase-dissonance", response_class=StreamingResponse)
def post_purchase_dissonance_chart():
    return get_post_purchase_dissonance_chart()

@app.get("/I8/community-engagement", response_class=Response)
def get_community_engagement_chart():
    return community_engagement_chart()

@app.get("/I7/user_segmentation", response_class=Response)
def get_user_segmentation_chart():
    return user_segmentation_proxy()

@app.get("/I13/subscription-interest", response_class=StreamingResponse)
def get_subscription_interest_chart():
    return generate_subscription_pie_chart()

@app.get("/I6/mobile-vs-desktop", response_class=StreamingResponse)
def get_mobile_desktop_chart():
    return generate_mobile_desktop_bar_chart()

@app.get("/I4/high-intent-keyword-trend")
def high_intent_keyword_trend():
    buf = generate_high_intent_keyword_trend_chart("KPI_Data/Keyword_Performance.csv")
    return StreamingResponse(buf, media_type="image/png")

@app.get("/I3/brand-switching", response_class=FileResponse)
def get_switch_trigger_chart():
    return generate_switch_trigger_chart()

@app.get("/I2/platform_funnel", response_class=FileResponse)
def platform_funnel_chart():
    return get_platform_funnel_kpi_chart()

@app.get("/I9/purchase-frequency", response_class=FileResponse)
def get_purchase_frequency_chart():
    return generate_purchase_frequency_chart()

@app.get("/I12/Return-issue-type", response_class=StreamingResponse)
def issue_type_chart():
    return generate_issue_type_chart()

@app.get("/I15/cross-generation", response_class=StreamingResponse)
def get_cross_generation_chart():
    return generate_cross_generation_chart()

@app.get("/I16/health-awareness", response_class=StreamingResponse)
def health_awareness_chart():
    return get_health_awareness_chart()

@app.get("/I17/recipe-usage")
def recipe_usage_chart():
    img_bytes = get_recipe_usage_figure_bytes("KPI_Data/recipe_integration_mentions.csv")
    return StreamingResponse(io.BytesIO(img_bytes), media_type="image/png")

@app.get("/I18/homemade-vs-local", response_class=StreamingResponse)
def get_homemade_vs_local_chart():
    return create_chart_image()

@app.get("/I19/impulse-chart", response_class=StreamingResponse)
def get_impulse_kpi_chart():
    return generate_impulse_kpi_chart()

@app.get("/I20/unboxing-sentiment", response_class=StreamingResponse)
def get_unboxing_chart():
    return get_unboxing_sentiment_chart()

@app.get("/I21/payment-issues", response_class=StreamingResponse)
def payment_issues_chart():
    return generate_payment_issues_chart()

@app.get("/I22/gift-card-user-type", response_class=StreamingResponse)
def gift_card_user_type():
    return create_user_type_pie_chart()

@app.get("/I23/hacktype-chart", response_class=StreamingResponse)
def hacktype_chart():
    return generate_hacktype_bar_chart()

@app.get("/I25/information-overload", response_class=StreamingResponse)
def information_overload_chart():
    return generate_information_overload_chart()

@app.get("/I29/influence-analysis", response_class=StreamingResponse)
def influence_analysis():
    return generate_influence_chart()

@app.get("/I30/price-increase-sentiment")
def price_increase_sentiment_chart():
    labels, sizes = load_reactions("KPI_Data/price_increase_reactions.csv")
    buf = create_pie_chart(labels, sizes)
    return StreamingResponse(buf, media_type="image/png")

# Section H : Advanced Haldiram Brand performance analysis
from fastapi import FastAPI, Response, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
import numpy as np
from H_adv_analysis_kpi.KPI1 import get_attribute_frequency_chart
from H_adv_analysis_kpi.KPI2 import get_attribute_frequency_chart_kpi2_with_sentiment
from H_adv_analysis_kpi.KPI3 import get_kpi3_sheet1_campaign_timeline_chart
from H_adv_analysis_kpi.KPI4 import router as kpi4_router
from H_adv_analysis_kpi.KPI5 import get_kpi5_chart
from H_adv_analysis_kpi.KPI6 import read_kpi6_excel
from H_adv_analysis_kpi.KPI7 import get_brand_personality_radar
from H_adv_analysis_kpi.KPI8 import get_kpi8_dashboard_chart_and_data
from H_adv_analysis_kpi.KPI9 import get_kpi9_reviews_data
from H_adv_analysis_kpi.KPI10 import get_comparison_sheet_sections
from H_adv_analysis_kpi.KPI11 import get_docx_file_response
from H_adv_analysis_kpi.KPI12 import analyze_kpi12_data
from H_adv_analysis_kpi.KPI13 import get_conversion_funnel_chart_improved
from H_adv_analysis_kpi.KPI14 import analyze_data
from H_adv_analysis_kpi.KPI15 import get_sheet2_data
from H_adv_analysis_kpi.KPI16 import get_value_perception_charts
from H_adv_analysis_kpi.KPI17 import get_sheet1_data
from H_adv_analysis_kpi.KPI18 import get_kpi18_sheet5_data
from H_adv_analysis_kpi.KPI19 import get_kpi19_sheet1_data
from H_adv_analysis_kpi.KPI20 import get_kpi20_sheet2_data
from H_adv_analysis_kpi.KPI21 import get_kpi21_sheet1_data
from H_adv_analysis_kpi.KPI22 import get_category_pie_chart
from H_adv_analysis_kpi.KPI23 import get_kpi23_sheet1_data
from H_adv_analysis_kpi.KPI24 import get_kpi24_sheet3_data, get_kpi24_qualitative_assessment_details
from H_adv_analysis_kpi.KPI25 import get_crisis_sentiment_trends_chart

app.include_router(kpi4_router)

@app.get("/H1-attribute-frequency")
def attribute_frequency_kpi():
    img_bytes = get_attribute_frequency_chart()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H2-sentiment-breakdown")
def sentiment_breakdown_kpi2():
    img_bytes = get_attribute_frequency_chart_kpi2_with_sentiment()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H3-sheet2-chart")
def kpi3_sheet2_chart():
    img_bytes = get_kpi3_sheet1_campaign_timeline_chart()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H4-doc-file")
def serve_docx():
    response = get_docx_file_response()
    if response is None:
        raise HTTPException(status_code=404, detail="File not found")
    return response

@app.get("/H5-chart")
def kpi5_chart():
    img_bytes = get_kpi5_chart()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H6-data")
def get_kpi6_data():
    df = read_kpi6_excel()
    if df is None:
        raise HTTPException(status_code=400, detail="Error reading Excel file")
    df = df.replace([np.nan, np.inf, -np.inf], None)
    return df.to_dict(orient="records")

@app.get("/H7-brand-personality-radar")
def brand_personality_radar_kpi():
    img_bytes = get_brand_personality_radar()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H8-dashboard-image")
def get_dashboard_image():
    img_bytes, _ = get_kpi8_dashboard_chart_and_data()
    if not img_bytes:
        raise HTTPException(404, "No data available to generate chart")
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H8-dashboard-data")
def get_dashboard_data():
    img_bytes, df = get_kpi8_dashboard_chart_and_data()
    if df.empty:
        raise HTTPException(404, "No data available in Sheet3")
    return JSONResponse({
        "chart_url": "/H/kpi8/dashboard-image",
        "sheet3_data": df.replace({np.nan: None}).to_dict(orient="records")
    })

@app.get("/H9-reviews")
def kpi9_reviews():
    try:
        return get_kpi9_reviews_data()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading KPI-9 file: {e}")

@app.get("/H10-comparison-full")
def comparison_full():
    try:
        return get_comparison_sheet_sections()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing Comparison sheet: {e}")

@app.get("/H11-doc-file")
def serve_docx():
    response = get_docx_file_response()
    if response is None:
        raise HTTPException(status_code=404, detail="File not found")
    return response

@app.get("/H12-results")
def get_kpi12_results():
    results = analyze_kpi12_data()
    if not results:
        raise HTTPException(status_code=404, detail="KPI data not found")
    return results

@app.get("/H13-conversion-funnel")
def conversion_funnel_kpi():
    img_bytes = get_conversion_funnel_chart_improved()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H14-results")
def get_kpi14_results():
    results = analyze_data()
    if not results:
        raise HTTPException(
            status_code=404,
            detail="KPI data not found",
            headers={"X-Error": "KPI14_DATA_MISSING"}
        )
    return {
        "status": "success",
        "results": results,
        "count": len(results)
    }

@app.get("/H15-sheet2")
def get_kpi15_sheet2():
    results = get_sheet2_data()
    if not results:
        raise HTTPException(status_code=404, detail="No data found in Sheet2 of KPI-15.xlsx")
    return {
        "status": "success",
        "results": results,
        "count": len(results)
    }

@app.get("/H16-value-perception-charts")
def value_perception_kpi():
    img_bytes = get_value_perception_charts()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

@app.get("/H17-sheet1")
def get_kpi17_sheet1():
    try:
        results = get_sheet1_data()
        if not results:
            raise HTTPException(status_code=404, detail="No data found in Sheet1 of KPI-17.xlsx")
        return {"status": "success", "results": results, "count": len(results)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Excel file not found")

@app.get("/H18-sheet5")
def get_kpi18_sheet5():
    results = get_kpi18_sheet5_data()
    if not results:
        raise HTTPException(status_code=404, detail="No data found in Sheet5 of KPI-18.xlsx")
    return {"status": "success", "results": results, "count": len(results)}

@app.get("/H19-sheet1")
def get_kpi19_sheet1():
    results = get_kpi19_sheet1_data()
    if not results:
        raise HTTPException(status_code=404, detail="No data found in Sheet1 of KPI-19.xlsx")
    return {"status": "success", "results": results, "count": len(results)}

@app.get("/H20-sheet2")
def get_kpi20_sheet2():
    results = get_kpi20_sheet2_data()
    if not results:
        raise HTTPException(status_code=404, detail="No data found in Sheet2 of KPI-20.xlsx")
    return {"status": "success", "results": results, "count": len(results)}

@app.get("/H21-sheet1")
def get_kpi21_sheet1():
    results = get_kpi21_sheet1_data()
    if not results:
        raise HTTPException(status_code=404, detail="No data found in Sheet1 of KPI-21.xlsx")
    return {"status": "success", "results": results, "count": len(results)}

@app.get("/H22-category-pie-chart")
def category_pie_chart_kpi():
    img_bytes = get_category_pie_chart()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")


@app.get("/H24-qualitative-assessment")
def get_kpi24_qualitative_assessment():
    results = get_kpi24_qualitative_assessment_details()
    if not results:
        raise HTTPException(
            status_code=404,
            detail="No qualitative assessment details found in Sheet3 of KPI-24.xlsx",
            headers={"X-Error": "QUALITATIVE_ASSESSMENT_MISSING"}
        )
    return {
        "status": "success",
        "results": results,
        "count": len(results)
    }

@app.get("/H25-brand-resilience-score")
def brand_resilience_score():
    img_bytes = get_crisis_sentiment_trends_chart()
    if not img_bytes:
        return {"message": "No data available to plot"}
    return Response(content=img_bytes, media_type="image/png")

# Section D : consumer insights
from fastapi import FastAPI
from D_Physical_KPI import (
    KPI1,KPI2, KPI3, KPI4, KPI5, KPI6, KPI7, KPI8,
    KPI9, KPI10, KPI11, KPI12, KPI13, KPI14, KPI15
)

# ✅ Register all 15 KPI Routers
app.include_router(KPI1.router, prefix="/D1")
app.include_router(KPI2.router, prefix="/D2")
app.include_router(KPI3.router, prefix="/D3")
app.include_router(KPI4.router, prefix="/D4")
app.include_router(KPI5.router, prefix="/D5")
app.include_router(KPI6.router, prefix="/D6")
app.include_router(KPI7.router, prefix="/D7")
app.include_router(KPI8.router, prefix="/D8")
app.include_router(KPI9.router, prefix="/D9")
app.include_router(KPI10.router, prefix="/D10")
app.include_router(KPI11.router, prefix="/D11")
app.include_router(KPI12.router, prefix="/D12")
app.include_router(KPI13.router, prefix="/D13")
app.include_router(KPI14.router, prefix="/D14")
app.include_router(KPI15.router, prefix="/D15")


# Section F : Advance market and category dynamics

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from section_Fcode import (
    main_api1, main_api2,  main_api3,  main_api4,  main_api5,  main_api6,  main_api7, 
     main_api8,  main_api9,  main_api10,  main_api11,  main_api12,  main_api13,  main_api14,
      main_api15,  main_api16,  main_api17,  main_api18,  main_api19,  main_api20
)

# ✅ Enable CORS for Swagger & frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers from individual API modules
app.include_router(main_api1.app.router, prefix="/F1")
app.include_router(main_api2.app.router, prefix="/F2")
app.include_router(main_api3.app.router, prefix="/F3")
app.include_router(main_api4.app.router, prefix="/F4")
app.include_router(main_api5.app.router, prefix="/F5")
app.include_router(main_api6.app.router, prefix="/F6")
app.include_router(main_api7.app.router, prefix="/F7")
app.include_router(main_api8.app.router, prefix="/F8")
app.include_router(main_api9.app.router, prefix="/F9")
app.include_router(main_api10.app.router, prefix="/F10")
app.include_router(main_api11.app.router, prefix="/F11")
app.include_router(main_api12.app.router, prefix="/F12")
app.include_router(main_api13.app.router, prefix="/F13")
app.include_router(main_api14.app.router, prefix="/F14")
app.include_router(main_api15.app.router, prefix="/F15")
app.include_router(main_api16.app.router, prefix="/F16")
app.include_router(main_api17.app.router, prefix="/F17")
app.include_router(main_api18.app.router, prefix="/F18")
app.include_router(main_api19.app.router, prefix="/F19")
app.include_router(main_api20.app.router, prefix="/F20")


# A section (Market)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi import Query
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
import io

from apis import (
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15
)

@app.get("/A-kpi/1")
async def run_kpi_1(request: Request):
    params = dict(request.query_params)
    return k1.run_kpi(params)

from fastapi import Query

@app.get("/kpi2/data")
async def get_kpi2_data(
    file_path: str = Query(
        default="Market_data/KPI-2.csv", 
        include_in_schema=False
    )
):
    params = {"file_path": file_path}
    result = k2.run_kpi(params)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/kpi2/plot")
async def get_kpi_5_plot(
    file_path: str = Query(
        default="Market_data/KPI-2.csv", 
        include_in_schema=False
    )
):
    try:
        buf = k2.generate_plot_image(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return StreamingResponse(buf, media_type="image/png")


@app.get("/A-kpi/3")
async def run_kpi_3(request: Request):
    params = dict(request.query_params)
    return k3.run_kpi(params)

@app.get("/A-kpi/4")
async def run_kpi_4(request: Request):
    params = dict(request.query_params)
    return k4.run_kpi(params)

# ...existing code...
from fastapi import Request, Query, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

@app.get("/A-kpi/5")
async def run_kpi_5():
    params = {"file_path": r"Market_data/KPI-5.csv"}
    result = k5.run_kpi(params)
    return JSONResponse(content=result)

@app.get("/A-kpi/5/plot")
async def get_kpi_5_plot(
    file_path: str = Query(
        default=r"Market_data/KPI-5.csv",
        include_in_schema=False
    )
):
    try:
        buf = k5.get_plot_image(file_path)
        return StreamingResponse(buf, media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating plot: {str(e)}")

@app.get("/A-kpi/6")
async def get_kpi_6(request: Request):
    params = dict(request.query_params)
    return k6.run_kpi(params)

@app.get("/A-kpi/6/plot")
async def get_kpi_6_plot(request: Request):
    params = dict(request.query_params)
    file_path = params.get("file_path", "Market_data/KPI-6.csv")
    img_buffer = k6.generate_plot_image(file_path)
    return StreamingResponse(img_buffer, media_type="image/png")

@app.get("/A-kpi/7")
async def run_kpi_7(request: Request):
    params = dict(request.query_params)
    return k7.run_kpi(params)

# ...existing code...
from fastapi import Request, Query, HTTPException
from fastapi.responses import StreamingResponse
import base64

@app.get("/A-kpi/8")
async def run_kpi_8(request: Request):
    params = dict(request.query_params)
    return k8.run_kpi(params)
@app.get("/A-kpi/8/plot", response_class=StreamingResponse)
async def get_kpi_8_plot(request: Request):
    params = dict(request.query_params)
    result = k8.run_kpi(params)

    if "chart_base64" in result and result["chart_base64"]:
        image_data = base64.b64decode(result["chart_base64"])
        return StreamingResponse(io.BytesIO(image_data), media_type="image/png")
    else:
        return JSONResponse(content={"error": "Chart not available"}, status_code=500)
    
@app.get("/A-kpi/9")
async def run_kpi_9(request: Request):
    params = dict(request.query_params)
    return k9.run_kpi_9(**params)


from fastapi import Query

@app.get("/A-kpi/10")
async def run_kpi_10(
    file_path: str = Query(
        default=r"Market_data/KPI-10.csv",
        include_in_schema=False
    )
):
    params = {"file_path": file_path}
    try:
        result = k10.run_kpi(params)
        return jsonable_encoder(result)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing KPI: {str(e)}")

@app.get("/A-kpi/10/plot")
async def get_kpi_10_plot(
    file_path: str = Query(
        default=r"Market_data/KPI-10.csv",
        include_in_schema=False
    )
):
    try:
        buf = k10.get_plot_image(file_path)
        return StreamingResponse(buf, media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating plot: {str(e)}")

from fastapi import Query, Request

@app.get("/A-kpi/11")
async def run_kpi_11():
    params = {"file_path": r"Market_data/KPI-11.csv"}
    try:
        result = k11.run_kpi(params)
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing KPI: {str(e)}")

@app.get("/A-kpi/11/plot")
async def get_kpi_11_plot(
    file_path: str = Query(
        default=r"Market_data/KPI-11.csv",
        include_in_schema=False
    )
):
    try:
        buf = k11.get_plot_image(file_path)
        return StreamingResponse(buf, media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating plot: {str(e)}")

@app.get("/A-kpi/12")
async def run_kpi_12(request: Request):
    params = dict(request.query_params)
    return k12.run_kpi(params)

@app.get("/A-kpi/13")
async def run_kpi_13(request: Request):
    params = dict(request.query_params)
    return k13.run_kpi(params)

@app.get("/A-kpi/14")
async def run_kpi_14(request: Request):
    params = dict(request.query_params)
    return k14.run_kpi(params)

@app.get("/A-kpi/15")
async def run_kpi_15(request: Request):
    params = dict(request.query_params)
    return k15.run_kpi(params)

from fastapi import Query

@app.get("/A-kpi/15/plot")
async def run_kpi_15_plot(
    file_path: str = Query(default="market_data/KPI-15.csv", include_in_schema=False)
):
    try:
        result = k15.run_kpi({"file_path": file_path})
        if "chart_buffer" in result:
            return StreamingResponse(result["chart_buffer"], media_type="image/png")
        raise HTTPException(status_code=400, detail="Plot not generated.")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found.")
    except Exception as e:
        print("KPI-15 Plot Error:", e)
        raise HTTPException(status_code=400, detail=f"Error generating plot: {str(e)}")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


