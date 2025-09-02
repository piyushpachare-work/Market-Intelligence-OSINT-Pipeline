from fastapi import FastAPI, Response
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np

app = FastAPI()

def generate_kpi10_chart(csv_filepath='section_FCSV/KPI10.csv', period='Q'):
    # Load and preprocess CSV (same as your analysis, simplified)
    df = pd.read_csv(csv_filepath, encoding='utf-8-sig')
    # Rename columns to your expected names for consistency
    rename_map = {
        df.columns[0]: 'Date',
        df.columns[1]: 'Event_Type',
        df.columns[2] if len(df.columns) > 2 else None: 'Companies_Involved',
        df.columns[3] if len(df.columns) > 3 else None: 'Description',
        df.columns[4] if len(df.columns) > 4 else None: 'Significance_Level',
        df.columns[5] if len(df.columns) > 5 else None: 'Action_Detail',
    }
    rename_map = {k:v for k,v in rename_map.items() if k is not None}
    df.rename(columns=rename_map, inplace=True)
    
    df['Significance_Level'] = df.get('Significance_Level', 'N/A').astype(str).str.strip().fillna('N/A')
    df['Event_Type'] = df['Event_Type'].astype(str).str.strip().fillna('Unknown Event')
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date', 'Event_Type'], inplace=True)
    
    # Filter for 'Major' significance
    consolidation_events_df = df[df['Significance_Level'].str.contains('Major', case=False, na=False)].copy()
    
    # Aggregate by period & event type
    consolidation_events_df['Period'] = consolidation_events_df['Date'].dt.to_period(period)
    event_counts = consolidation_events_df.groupby(['Period', 'Event_Type']).size().unstack(fill_value=0)
    
    # Plot stacked bar chart
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 8))
    
    if period == 'Q':
        x_labels = [f"{p.year} Q{p.quarter}" for p in event_counts.index]
        x_axis_label = "Quarter"
    else:
        x_labels = [str(p.year) for p in event_counts.index]
        x_axis_label = "Year"
    
    event_counts.plot(kind='bar', stacked=True, ax=ax, colormap='viridis', edgecolor='black', alpha=0.85)
    
    ax.set_title(f'Market Consolidation Activity Index\n("Major" Events by Type per {x_axis_label})', fontsize=16, pad=15)
    ax.set_xlabel(x_axis_label, fontsize=12, labelpad=10)
    ax.set_ylabel('Number of "Major" Consolidation Events', fontsize=12, labelpad=10)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=10)
    
    max_total = event_counts.sum(axis=1).max()
    if pd.notna(max_total) and max_total > 0:
        ax.set_yticks(np.arange(0, max_total + 2, step=max(1, int(max_total/5))))
    else:
        ax.set_yticks(np.arange(0, 2, 1))
    plt.yticks(fontsize=10)
    
    ax.grid(True, axis='y', linestyle=':', alpha=0.7)
    ax.grid(False, axis='x')
    
    ax.legend(title='Event Type', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0., fontsize=9)
    
    for i, total in enumerate(event_counts.sum(axis=1)):
        if total > 0:
            ax.text(i, total + 0.1, int(total), ha='center', va='bottom', fontsize=9, weight='bold')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.92])
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()

@app.get("/F/kpi10")
async def kpi10_chart():
    try:
        image_bytes = generate_kpi10_chart()
        return Response(content=image_bytes, media_type="image/png")
    except FileNotFoundError:
        return Response(content="CSV file KPI10.csv not found.".encode(), status_code=404)
    except Exception as e:
        return Response(content=f"Error generating chart: {e}".encode(), status_code=500)
