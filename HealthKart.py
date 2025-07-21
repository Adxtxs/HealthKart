import pandas as pd
import numpy as np
import datetime
import uuid

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# --- 1. Data Modeling---

def generate_uuid():
    """Generates a random UUID."""
    return str(uuid.uuid4())

def get_random_date(start_date, end_date):
    """Generates a random date between two given dates."""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = np.random.randint(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

def generate_mock_data(num_influencers=20, num_posts_per_influencer=5, num_tracking_entries_per_post=3):
    """Generates mock data for influencers, posts, tracking_data, and payouts."""

    categories = ['Fitness', 'Beauty', 'Nutrition', 'Lifestyle', 'Gaming']
    genders = ['Male', 'Female', 'Other']
    platforms = ['Instagram', 'YouTube', 'Twitter']
    brands = ['MuscleBlaze', 'HKVitals', 'Gritzo', 'TrueBasics']
    products = ['Protein Powder', 'Multivitamin', 'Kids Nutrition', 'Omega-3', 'Creatine', 'Hair Gummies']

    influencers_data = []
    posts_data = []
    tracking_data_list = []
    payouts_data = []

    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 12, 31)

    for i in range(num_influencers):
        influencer_id = generate_uuid()
        follower_count = np.random.randint(10000, 1000000) # 10k to 1M

        influencers_data.append({
            'ID': influencer_id,
            'name': f'Influencer {i + 1}',
            'category': np.random.choice(categories),
            'gender': np.random.choice(genders),
            'follower_count': follower_count,
            'platform': np.random.choice(platforms) # Primary platform
        })

        for j in range(num_posts_per_influencer):
            post_id = generate_uuid()
            post_platform = np.random.choice(platforms)
            post_date = get_random_date(start_date, end_date)
            
            reach = int(follower_count * np.random.uniform(0.2, 0.8))
            likes = int(reach * np.random.uniform(0.01, 0.1))
            comments = int(likes * np.random.uniform(0.01, 0.1))

            posts_data.append({
                'influencer_id': influencer_id,
                'platform': post_platform,
                'date': post_date,
                'URL': f'https://{post_platform}.com/post/{post_id}',
                'caption': f'Check out this amazing {np.random.choice(products)} from {np.random.choice(brands)}! #ad #healthkart',
                'reach': reach,
                'likes': likes,
                'comments': comments
            })

            basis = np.random.choice(['post', 'order'])
            rate = np.random.uniform(500, 5000) if basis == 'post' else np.random.uniform(0.5, 10) # 500-5000 per post, 0.5-10 per order

            total_orders_for_post = 0
            for k in range(num_tracking_entries_per_post):
                tracking_date = get_random_date(datetime.datetime.strptime(post_date, '%Y-%m-%d').date(),
                                                datetime.datetime.strptime(post_date, '%Y-%m-%d').date() + datetime.timedelta(days=30))
                num_orders = np.random.randint(1, 50) # 1 to 50 orders
                revenue_per_order = np.random.randint(200, 1500) # 200 to 1500 per order
                total_revenue_entry = num_orders * revenue_per_order

                tracking_data_list.append({
                    'source': post_platform,
                    'campaign': f'Campaign-{np.random.randint(1, 5)}',
                    'influencer_id': influencer_id,
                    'user_id': generate_uuid(),
                    'product': np.random.choice(products),
                    'brand': np.random.choice(brands), # Added brand for filtering
                    'date': tracking_date,
                    'orders': num_orders,
                    'revenue': total_revenue_entry
                })
                total_orders_for_post += num_orders
            
            total_payout = rate if basis == 'post' else total_orders_for_post * rate
            payouts_data.append({
                'influencer_id': influencer_id,
                'basis': basis,
                'rate': rate,
                'orders': total_orders_for_post, # Total orders linked to this payout entry
                'total_payout': total_payout
            })

    influencers_df = pd.DataFrame(influencers_data)
    posts_df = pd.DataFrame(posts_data)
    tracking_data_df = pd.DataFrame(tracking_data_list)
    payouts_df = pd.DataFrame(payouts_data)

    return influencers_df, posts_df, tracking_data_df, payouts_df

# Generate initial data
influencers_df, posts_df, tracking_data_df, payouts_df = generate_mock_data()

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css' # Font Awesome 6
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className="min-h-screen bg-gray-100 font-inter p-4 sm:p-6 md:p-8", children=[
    html.Div(className="max-w-7xl mx-auto bg-white rounded-xl shadow-lg p-4 sm:p-6 md:p-8", children=[
        html.H1("HealthKart Influencer Dashboard", className="text-3xl sm:text-4xl font-bold text-gray-800 mb-6 text-center"),

        # Data Ingestion Section
        html.Div(className="bg-blue-50 p-4 rounded-lg flex flex-col sm:flex-row items-center justify-between mb-6 shadow-sm", children=[
            html.P("Simulate Data Ingestion:", className="text-blue-800 text-lg font-medium mb-3 sm:mb-0"),
            html.Button(
                "Generate New Mock Data",
                id="generate-data-button",
                n_clicks=0,
                className="flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors text-lg font-semibold"
            ),
            html.Div(id="data-generation-status", className="absolute top-4 right-4")
        ]),

        # Filters Section
        html.Div(className="bg-gray-50 p-4 rounded-lg mb-6 shadow-sm", children=[
            html.H2(html.Span([html.I(className="fas fa-filter mr-2 text-gray-600"), "Filters"]), className="text-xl font-semibold text-gray-700 mb-4 flex items-center"),
            html.Div(className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children=[
                html.Div(children=[
                    html.Label("Brand", className="block text-sm font-medium text-gray-700 mb-1"),
                    dcc.Dropdown(
                        id='brand-filter',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': brand, 'value': brand} for brand in sorted(tracking_data_df['brand'].unique())],
                        value='All',
                        clearable=False,
                        className="mt-1 block w-full text-base rounded-md shadow-sm"
                    )
                ]),
                html.Div(children=[
                    html.Label("Product", className="block text-sm font-medium text-gray-700 mb-1"),
                    dcc.Dropdown(
                        id='product-filter',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': product, 'value': product} for product in sorted(tracking_data_df['product'].unique())],
                        value='All',
                        clearable=False,
                        className="mt-1 block w-full text-base rounded-md shadow-sm"
                    )
                ]),
                html.Div(children=[
                    html.Label("Influencer Category", className="block text-sm font-medium text-gray-700 mb-1"),
                    dcc.Dropdown(
                        id='influencer-category-filter',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': category, 'value': category} for category in sorted(influencers_df['category'].unique())],
                        value='All',
                        clearable=False,
                        className="mt-1 block w-full text-base rounded-md shadow-sm"
                    )
                ]),
                html.Div(children=[
                    html.Label("Platform", className="block text-sm font-medium text-gray-700 mb-1"),
                    dcc.Dropdown(
                        id='platform-filter',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': platform, 'value': platform} for platform in sorted(tracking_data_df['source'].unique())],
                        value='All',
                        clearable=False,
                        className="mt-1 block w-full text-base rounded-md shadow-sm"
                    )
                ])
            ])
        ]),

        # Campaign Performance Section
        html.Div(className="mb-8", children=[
            html.H2("Campaign Performance", className="text-2xl font-bold text-gray-800 mb-4 text-center"),
            html.Div(className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8", children=[
                html.Div(className="bg-white p-5 rounded-lg shadow-md flex items-center justify-between", children=[
                    html.Div(children=[
                        html.P("Total Revenue", className="text-gray-500 text-sm"),
                        html.P(id="total-revenue", className="text-2xl font-semibold text-gray-900")
                    ]),
                    html.Div(className="p-3 bg-green-100 rounded-full text-green-600", children=html.I(className="fas fa-dollar-sign text-xl"))
                ]),
                html.Div(className="bg-white p-5 rounded-lg shadow-md flex items-center justify-between", children=[
                    html.Div(children=[
                        html.P("Total Orders", className="text-gray-500 text-sm"),
                        html.P(id="total-orders", className="text-2xl font-semibold text-gray-900")
                    ]),
                    html.Div(className="p-3 bg-blue-100 rounded-full text-blue-600", children=html.I(className="fas fa-shopping-cart text-xl"))
                ]),
                html.Div(className="bg-white p-5 rounded-lg shadow-md flex items-center justify-between", children=[
                    html.Div(children=[
                        html.P("Total Payout", className="text-gray-500 text-sm"),
                        html.P(id="total-payout", className="text-2xl font-semibold text-gray-900")
                    ]),
                    html.Div(className="p-3 bg-red-100 rounded-full text-red-600", children=html.I(className="fas fa-money-bill-wave text-xl"))
                ]),
                html.Div(className="bg-white p-5 rounded-lg shadow-md flex items-center justify-between", children=[
                    html.Div(children=[
                        html.P("ROAS", className="text-gray-500 text-sm"),
                        html.P(id="roas", className="text-2xl font-semibold text-gray-900")
                    ]),
                    html.Div(className="p-3 bg-purple-100 rounded-full text-purple-600", children=html.I(className="fas fa-chart-line text-xl"))
                ]),
                html.Div(className="bg-white p-5 rounded-lg shadow-md flex items-center justify-between", children=[
                    html.Div(children=[
                        html.P("Incremental ROAS", className="text-gray-500 text-sm"),
                        html.P(id="incremental-roas", className="text-2xl font-semibold text-gray-900")
                    ]),
                    html.Div(className="p-3 bg-teal-100 rounded-full text-teal-600", children=html.I(className="fas fa-chart-area text-xl"))
                ])
            ]),

            html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6", children=[
                html.Div(className="bg-white p-6 rounded-lg shadow-md", children=[
                    html.H3("Revenue Over Time", className="text-lg font-semibold text-gray-800 mb-4"),
                    dcc.Graph(id='revenue-over-time-chart', config={'displayModeBar': False})
                ]),
                html.Div(className="bg-white p-6 rounded-lg shadow-md", children=[
                    html.H3("Revenue by Platform", className="text-lg font-semibold text-gray-800 mb-4"),
                    dcc.Graph(id='revenue-by-platform-chart', config={'displayModeBar': False})
                ]),
                html.Div(className="bg-white p-6 rounded-lg shadow-md lg:col-span-2", children=[
                    html.H3("Revenue by Campaign", className="text-lg font-semibold text-gray-800 mb-4"),
                    dcc.Graph(id='revenue-by-campaign-chart', config={'displayModeBar': False})
                ])
            ])
        ]),

        # Influencer Insights Section
        html.Div(className="mb-8", children=[
            html.H2("Influencer Insights", className="text-2xl font-bold text-gray-800 mb-4 text-center"),
            html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6", children=[
                html.Div(className="bg-white p-6 rounded-lg shadow-md", children=[
                    html.H3("Top 5 Influencers by Revenue", className="text-lg font-semibold text-gray-800 mb-4"),
                    html.Div(id="top-influencers-revenue-table", className="overflow-x-auto")
                ]),
                html.Div(className="bg-white p-6 rounded-lg shadow-md", children=[
                    html.H3("Top 5 Influencers by ROAS", className="text-lg font-semibold text-gray-800 mb-4"),
                    html.Div(id="top-influencers-roas-table", className="overflow-x-auto")
                ]),
                html.Div(className="bg-white p-6 rounded-lg shadow-md", children=[
                    html.H3("Best Performing Personas (by Avg. ROAS)", className="text-lg font-semibold text-gray-800 mb-4"),
                    html.Div(id="best-personas-table", className="overflow-x-auto")
                ]),
                html.Div(className="bg-white p-6 rounded-lg shadow-md", children=[
                    html.H3("Poor ROIs (ROAS < 1)", className="text-lg font-semibold text-gray-800 mb-4"),
                    html.Div(id="poor-rois-table", className="overflow-x-auto")
                ])
            ])
        ]),

        # Payout Tracking Section
        html.Div(className="mb-8", children=[
            html.H2("Payout Tracking", className="text-2xl font-bold text-gray-800 mb-4 text-center"),
            html.Div(className="bg-white p-6 rounded-lg shadow-md", children=[
                html.H3("Detailed Payouts", className="text-lg font-semibold text-gray-800 mb-4"),
                html.Div(id="payouts-table", className="overflow-x-auto")
            ])
        ]),

        # Export Section
        html.Div(className="bg-blue-50 p-4 rounded-lg flex flex-col sm:flex-row items-center justify-between shadow-sm", children=[
            html.P("Export Current Data:", className="text-blue-800 text-lg font-medium mb-3 sm:mb-0"),
            html.Button(
                "Export Filtered Data to CSV",
                id="export-csv-button",
                n_clicks=0,
                className="flex items-center px-6 py-3 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 transition-colors text-lg font-semibold"
            ),
            dcc.Download(id="download-dataframe-csv")
        ]),

        # Hidden Div to store filtered data for export and calculations
        dcc.Store(id='filtered-tracking-data-store'),
        dcc.Store(id='filtered-payouts-data-store'),
        dcc.Store(id='filtered-influencers-data-store'), # To pass influencer details for insights
        dcc.Store(id='filtered-posts-data-store') # To pass post details for insights
    ])
])

#Callbacks

@app.callback(
    [Output('data-generation-status', 'children'),
     Output('filtered-tracking-data-store', 'data'),
     Output('filtered-payouts-data-store', 'data'),
     Output('filtered-influencers-data-store', 'data'),
     Output('filtered-posts-data-store', 'data'),
     Output('brand-filter', 'options'),
     Output('product-filter', 'options'),
     Output('influencer-category-filter', 'options'),
     Output('platform-filter', 'options')],
    [Input('generate-data-button', 'n_clicks')]
)
def update_data(n_clicks):
    global influencers_df, posts_df, tracking_data_df, payouts_df # Declare as global to modify
    if n_clicks > 0:
        influencers_df, posts_df, tracking_data_df, payouts_df = generate_mock_data()
        status_message = html.Div(
            "Data Generated Successfully!",
            className="bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg flex items-center"
        )
    else:
        status_message = "" # No message on initial load

    # Update filter options based on new data
    unique_brands = [{'label': 'All', 'value': 'All'}] + [{'label': brand, 'value': brand} for brand in sorted(tracking_data_df['brand'].unique())]
    unique_products = [{'label': 'All', 'value': 'All'}] + [{'label': product, 'value': product} for product in sorted(tracking_data_df['product'].unique())]
    unique_influencer_categories = [{'label': 'All', 'value': 'All'}] + [{'label': category, 'value': category} for category in sorted(influencers_df['category'].unique())]
    unique_platforms = [{'label': 'All', 'value': 'All'}] + [{'label': platform, 'value': platform} for platform in sorted(tracking_data_df['source'].unique())]

    return (
        status_message,
        tracking_data_df.to_dict('records'),
        payouts_df.to_dict('records'),
        influencers_df.to_dict('records'),
        posts_df.to_dict('records'),
        unique_brands,
        unique_products,
        unique_influencer_categories,
        unique_platforms
    )

@app.callback(
    [Output('total-revenue', 'children'),
     Output('total-orders', 'children'),
     Output('total-payout', 'children'),
     Output('roas', 'children'),
     Output('incremental-roas', 'children'),
     Output('revenue-over-time-chart', 'figure'),
     Output('revenue-by-platform-chart', 'figure'),
     Output('revenue-by-campaign-chart', 'figure'),
     Output('top-influencers-revenue-table', 'children'),
     Output('top-influencers-roas-table', 'children'),
     Output('best-personas-table', 'children'),
     Output('poor-rois-table', 'children'),
     Output('payouts-table', 'children')],
    [Input('brand-filter', 'value'),
     Input('product-filter', 'value'),
     Input('influencer-category-filter', 'value'),
     Input('platform-filter', 'value'),
     Input('filtered-tracking-data-store', 'data'),
     Input('filtered-payouts-data-store', 'data'),
     Input('filtered-influencers-data-store', 'data'),
     Input('filtered-posts-data-store', 'data')]
)
def update_dashboard(selected_brand, selected_product, selected_influencer_category, selected_platform,
                     stored_tracking_data, stored_payouts_data, stored_influencers_data, stored_posts_data):

    # Convert stored data back to DataFrames
    current_tracking_df = pd.DataFrame(stored_tracking_data)
    current_payouts_df = pd.DataFrame(stored_payouts_data)
    current_influencers_df = pd.DataFrame(stored_influencers_data)
    current_posts_df = pd.DataFrame(stored_posts_data)

    # Apply filters
    filtered_tracking_df = current_tracking_df.copy()
    if selected_brand != 'All':
        filtered_tracking_df = filtered_tracking_df[filtered_tracking_df['brand'] == selected_brand]
    if selected_product != 'All':
        filtered_tracking_df = filtered_tracking_df[filtered_tracking_df['product'] == selected_product]
    if selected_platform != 'All':
        filtered_tracking_df = filtered_tracking_df[filtered_tracking_df['source'] == selected_platform]

    # Filter by influencer category (requires joining with influencers_df)
    if selected_influencer_category != 'All':
        filtered_influencer_ids = current_influencers_df[
            current_influencers_df['category'] == selected_influencer_category
        ]['ID'].tolist()
        filtered_tracking_df = filtered_tracking_df[
            filtered_tracking_df['influencer_id'].isin(filtered_influencer_ids)
        ]
    
    # Filter payouts based on the filtered tracking data's influencer_ids
    # This ensures payouts are only for influencers whose tracking data matches the current filters
    filtered_payouts_df = current_payouts_df[
        current_payouts_df['influencer_id'].isin(filtered_tracking_df['influencer_id'].unique())
    ].copy()

    # --- KPIs ---
    total_revenue = filtered_tracking_df['revenue'].sum() if not filtered_tracking_df.empty else 0
    total_orders = filtered_tracking_df['orders'].sum() if not filtered_tracking_df.empty else 0
    total_payout = filtered_payouts_df['total_payout'].sum() if not filtered_payouts_df.empty else 0

    roas = (total_revenue / total_payout) if total_payout > 0 else 0
    incremental_revenue = total_revenue * 0.7 # Simplified assumption
    incremental_roas = (incremental_revenue / total_payout) if total_payout > 0 else 0

    # Format KPIs
    formatted_total_revenue = f"${total_revenue:,.2f}"
    formatted_total_orders = f"{int(total_orders):,}"
    formatted_total_payout = f"${total_payout:,.2f}"
    formatted_roas = f"{roas:.2f}" if roas != 0 else "N/A"
    formatted_incremental_roas = f"{incremental_roas:.2f}" if incremental_roas != 0 else "N/A"

    # --- Charts ---
    # Revenue Over Time
    revenue_by_date = filtered_tracking_df.groupby('date')['revenue'].sum().reset_index()
    revenue_by_date = revenue_by_date.sort_values('date')
    fig_revenue_over_time = px.line(revenue_by_date, x='date', y='revenue', title='Revenue Over Time',
                                    labels={'date': 'Date', 'revenue': 'Revenue ($)'},
                                    color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_revenue_over_time.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font_color='#333',
        xaxis_title=None, yaxis_title=None, margin=dict(l=20, r=20, t=40, b=20)
    )

    # Revenue by Platform
    revenue_by_platform = filtered_tracking_df.groupby('source')['revenue'].sum().reset_index()
    fig_revenue_by_platform = px.bar(revenue_by_platform, x='source', y='revenue', title='Revenue by Platform',
                                     labels={'source': 'Platform', 'revenue': 'Revenue ($)'},
                                     color='source', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_revenue_by_platform.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font_color='#333',
        xaxis_title=None, yaxis_title=None, margin=dict(l=20, r=20, t=40, b=20)
    )

    # Revenue by Campaign
    revenue_by_campaign = filtered_tracking_df.groupby('campaign')['revenue'].sum().reset_index()
    fig_revenue_by_campaign = px.bar(revenue_by_campaign, x='campaign', y='revenue', title='Revenue by Campaign',
                                     labels={'campaign': 'Campaign', 'revenue': 'Revenue ($)'},
                                     color='campaign', color_discrete_sequence=px.colors.qualitative.Set2)
    fig_revenue_by_campaign.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font_color='#333',
        xaxis_title=None, yaxis_title=None, margin=dict(l=20, r=20, t=40, b=20)
    )


    # --- Influencer Insights ---
    # Merge dataframes for comprehensive influencer performance
    influencer_performance_df = filtered_tracking_df.groupby('influencer_id').agg(
        totalRevenue=('revenue', 'sum'),
        totalOrders=('orders', 'sum')
    ).reset_index()

    payouts_agg = filtered_payouts_df.groupby('influencer_id')['total_payout'].sum().reset_index()
    influencer_performance_df = pd.merge(influencer_performance_df, payouts_agg, on='influencer_id', how='left').fillna(0)

    # Add post metrics (reach, likes, comments)
    posts_agg = current_posts_df.groupby('influencer_id').agg(
        totalReach=('reach', 'sum'),
        totalLikes=('likes', 'sum'),
        totalComments=('comments', 'sum')
    ).reset_index()
    influencer_performance_df = pd.merge(influencer_performance_df, posts_agg, on='influencer_id', how='left').fillna(0)

    # Merge with influencer details (name, category, platform, follower_count)
    influencer_performance_df = pd.merge(
        influencer_performance_df,
        current_influencers_df[['ID', 'name', 'category', 'platform', 'follower_count']],
        left_on='influencer_id',
        right_on='ID',
        how='left'
    ).drop(columns=['ID'])

    # Calculate ROAS and Incremental ROAS for each influencer
    influencer_performance_df['roas'] = influencer_performance_df.apply(
        lambda row: (row['totalRevenue'] / row['total_payout']) if row['total_payout'] > 0 else 0, axis=1
    )
    influencer_performance_df['incremental_roas'] = influencer_performance_df.apply(
        lambda row: (row['totalRevenue'] * 0.7 / row['total_payout']) if row['total_payout'] > 0 else 0, axis=1
    )

    # Top 5 Influencers by Revenue
    top_influencers_revenue = influencer_performance_df.sort_values(by='totalRevenue', ascending=False).head(5)
    top_influencers_revenue_table = generate_table(top_influencers_revenue[['name', 'totalRevenue', 'totalOrders', 'roas', 'platform']])

    # Top 5 Influencers by ROAS (only valid ROAS > 0)
    top_influencers_roas = influencer_performance_df[influencer_performance_df['roas'] > 0].sort_values(by='roas', ascending=False).head(5)
    top_influencers_roas_table = generate_table(top_influencers_roas[['name', 'roas', 'totalRevenue', 'total_payout', 'platform']])

    # Best Performing Personas (by Avg. ROAS)
    persona_performance = influencer_performance_df.groupby('category').agg(
        avg_roas=('roas', lambda x: x[x > 0].mean() if not x[x > 0].empty else 0), # Average of valid ROAS
        totalRevenue=('totalRevenue', 'sum'),
        totalPayout=('total_payout', 'sum'),
        influencerCount=('name', 'count')
    ).reset_index().sort_values(by='avg_roas', ascending=False)
    best_personas_table = generate_table(persona_performance)

    # Poor ROIs (ROAS < 1 and payout > 0)
    poor_rois = influencer_performance_df[(influencer_performance_df['roas'] < 1) & (influencer_performance_df['total_payout'] > 0)].sort_values(by='roas', ascending=True).head(5)
    poor_rois_table = generate_table(poor_rois[['name', 'roas', 'totalRevenue', 'total_payout', 'platform']])

    # Payout Tracking Table
    payouts_table = generate_table(filtered_payouts_df[['influencer_id', 'basis', 'rate', 'orders', 'total_payout']])

    return (
        formatted_total_revenue,
        formatted_total_orders,
        formatted_total_payout,
        formatted_roas,
        formatted_incremental_roas,
        fig_revenue_over_time,
        fig_revenue_by_platform,
        fig_revenue_by_campaign,
        top_influencers_revenue_table,
        top_influencers_roas_table,
        best_personas_table,
        poor_rois_table,
        payouts_table
    )

def generate_table(dataframe):
    """Generates an HTML table from a pandas DataFrame."""
    if dataframe.empty:
        return html.P("No data available for this selection.", className="text-gray-600 text-center py-4")

    # Create a copy to avoid SettingWithCopyWarning
    df_copy = dataframe.copy()

    # Format currency columns
    for col in ['totalRevenue', 'total_payout', 'rate']:
        if col in df_copy.columns:
            df_copy.loc[:, col] = df_copy[col].apply(lambda x: f"${x:,.2f}")
    # Format ROAS columns
    for col in ['roas', 'incremental_roas', 'avg_roas']:
        if col in df_copy.columns:
            df_copy.loc[:, col] = df_copy[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) and x != 0 else "N/A")
    # Format orders
    for col in ['totalOrders', 'orders', 'follower_count', 'influencerCount', 'totalReach', 'totalLikes', 'totalComments']:
        if col in df_copy.columns:
            df_copy.loc[:, col] = df_copy[col].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "N/A")

    return html.Table(
        className="min-w-full divide-y divide-gray-200 rounded-lg overflow-hidden", # Added rounded-lg and overflow-hidden
        children=[
            html.Thead(
                className="bg-gray-100", # Slightly darker header
                children=html.Tr([html.Th(col, scope="col", className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider") for col in df_copy.columns])
            ),
            html.Tbody(
                className="bg-white divide-y divide-gray-200",
                children=[
                    html.Tr(
                        children=[html.Td(row[col], className="px-6 py-4 whitespace-nowrap text-sm text-gray-900") for col in df_copy.columns]
                    ) for index, row in df_copy.iterrows()
                ]
            )
        ]
    )

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("export-csv-button", "n_clicks"),
    [dash.dependencies.State('filtered-tracking-data-store', 'data'),
     dash.dependencies.State('filtered-payouts-data-store', 'data'),
     dash.dependencies.State('filtered-influencers-data-store', 'data'),
     dash.dependencies.State('filtered-posts-data-store', 'data')]
)
def export_csv(n_clicks, tracking_data_json, payouts_data_json, influencers_data_json, posts_data_json):
    if n_clicks > 0:
        # Convert JSON back to DataFrames
        tracking_df = pd.DataFrame(tracking_data_json)
        payouts_df = pd.DataFrame(payouts_data_json)
        influencers_df = pd.DataFrame(influencers_data_json)
        posts_df = pd.DataFrame(posts_data_json)

        # Create a dictionary of dataframes to export
        dfs_to_export = {
            "tracking_data": tracking_df,
            "payouts": payouts_df,
            "influencers": influencers_df,
            "posts": posts_df
        }

        # Create a zip file in memory
        import io
        import zipfile
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for df_name, df in dfs_to_export.items():
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                zip_file.writestr(f"{df_name}.csv", csv_buffer.getvalue())
        zip_buffer.seek(0)

        return dcc.send_bytes(zip_buffer.read(), "healthkart_influencer_data.zip")
    return None

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
