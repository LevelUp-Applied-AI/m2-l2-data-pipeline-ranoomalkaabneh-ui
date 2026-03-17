"""
Lab 2 — Data Pipeline: Retail Sales Analysis
Module 2 — Programming for AI & Data Science

Complete each function below. Remove the TODO: comments and pass statements
as you implement each function. Do not change the function signatures.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ─── Configuration ────────────────────────────────────────────────────────────

DATA_PATH = 'data/sales_records.csv'
OUTPUT_DIR = 'output'


# ─── Pipeline Functions ───────────────────────────────────────────────────────

def load_data(filepath):
   
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found")

    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records from {filepath}")
    return df


def clean_data(df):
    """Handle missing values and fix data types.
    """

    df = df.copy()  # Never modify the input in place

    df['quantity'] = df['quantity'].fillna(df['quantity'].median())
    df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.dropna(subset=['date'])

    print(f"Cleaned {len(df)} records")

    return df

def add_features(df):
    
       """Add revenue and day_of_week columns. Returns an enriched DataFrame."""
def add_features(df):
    """Compute derived columns. Returns an enriched DataFrame."""
    df = df.copy()
    df['revenue'] = df['quantity'] * df['unit_price']
    df['day_of_week'] = df['date'].dt.day_name()
    return df

def generate_summary(df):
    """Compute summary statistics. Returns a dict."""
    summary = {
        'total_revenue': float(df['revenue'].sum()),
        'avg_order_value': float(df['revenue'].mean()),
        'top_category': df.groupby('product_category')['revenue'].sum().idxmax(),
        'record_count': int(len(df))
    }

    return summary
    



def create_visualizations(df, output_dir='output'):
    """Generate and save 3 charts as PNG files following requirements."""
    
    import os
    import matplotlib.pyplot as plt
    
    os.makedirs(output_dir, exist_ok=True)

    # 1️⃣ Revenue by category
    fig, ax = plt.subplots()
    category_revenue = df.groupby('product_category')['revenue'].sum()
    category_revenue.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Revenue by Category")
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Revenue")
    fig.savefig(f'{output_dir}/revenue_by_category.png', dpi=150, bbox_inches='tight')
    plt.close(fig)  # Free memory

    # 2️⃣ Daily revenue trend
    fig, ax = plt.subplots()
    daily_revenue = df.groupby('date')['revenue'].sum().sort_index()
    daily_revenue.plot(ax=ax, color='green')
    ax.set_title("Daily Revenue Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    fig.savefig(f'{output_dir}/daily_revenue_trend.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # 3️⃣ Average order by payment method
    fig, ax = plt.subplots()
    avg_order = df.groupby('payment_method')['revenue'].mean()
    avg_order.plot(kind='bar', ax=ax, color='orange')
    ax.set_title("Average Order Value by Payment Method")
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Average Revenue")
    fig.savefig(f'{output_dir}/avg_order_by_payment.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

def main():
    df = load_data('data/sales_records.csv')
    df = clean_data(df)
    df = add_features(df)
    summary = generate_summary(df)
    print(summary)
    create_visualizations(df)

if __name__ == "__main__":
    main()