def compute_summary(df):
    summary = {
        'total_earthquakes': len(df),
        'max_magnitude': df['mag'].max(),
        'min_magnitude': df['mag'].min(),
        'avg_magnitude': round(df['mag'].mean(), 2)
    }
    return summary
