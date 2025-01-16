import pandas as pd
import streamlit as st

# Function to process each uploaded file
def process_excel(file, columns_reference=None, month=None):
    df = pd.read_excel(file, header=[0, 1, 2, 3, 4]).iloc[:, :18]  
    # Combine multi-level header into a single-level header
    df.columns = ['_'.join([str(col).strip() for col in col_tuple]) for col_tuple in df.columns.values]

    # Align column names if a reference is provided
    if columns_reference is not None:
        df.columns = columns_reference

    # Add a 'Month' column and fill it with the selected month
    if month is not None:
        df['Month'] = month

    return df

# Function to assign region based on 'POINT OF SALE'
def assign_region(df):
    # Defining the regions based on the 'POINT OF SALE' values
    far_east_values = [
        'AUSTRALIA', 'CHINA EAST', 'CHINA REST', 'CHINA SOUTH', 'HONG KONG', 'INDONESIA', 'JAPAN', 'MALAYSIA', 
        'NEW ZEALAND', 'PHILIPPINES', 'SINGAPORE', 'SOUTH KOREA', 'TAIWAN', 'THAILAND', 'UNION OF MYANMAR', 'VIETNAM'
    ]
    europe_values = [
        'AUSTRIA', 'BELGIUM', 'CANADA', 'CYPRUS', 'CZECH REPUBLIC', 'DENMARK', 'FINLAND', 'FRANCE', 'GERMANY', 
        'GREECE', 'ICELAND', 'IRELAND', 'ISRAEL', 'ITALY', 'LUXEMBOURG', 'NETHERLANDS', 'NORWAY', 'POLAND', 
        'PORTUGAL', 'RUSSIAN FEDERATION', 'SLOVAKIA', 'SPAIN', 'SWEDEN', 'SWITZERLAND', 'TURKEY', 'UNITED KINGDOM', 
        'UNITED STATES OF AMERICA'
    ]
    srilanka_values = ['SRI LANKA']
    india_values = [
        'INDIA AHMEDABAD', 'INDIA GOA', 'INDIA HYDERABAD', 'INDIA VISHAKHAPATNAM', 'INDIA KARNATAKA', 
        'INDIA KERALA - COCHIN', 'INDIA KERALA CALICUT', 'INDIA EASTERN KOLKATA', 'INDIA NORTHERN', 
        'INDIA TAMILNADU - CHENNAI', 'INDIA TAMILNADU COIMBATORE', 'INDIA TAMILNADU-MADURAI', 'INDIA TAMILNADU TIRICHI', 
        'INDIA TRIVANDRUM', 'INDIA WESTERN'
    ]
    m_east_and_africa_values = [
        'ABU DHABI & AL AIN', 'Dubai', 'Dubai - SHARJAH', 'Dubai - NORTHERN EMIRATES', 'BAHRAIN', 'KUWAIT', 'OMAN', 
        'QATAR', 'SEYCHELLES', 'SAUDI CENTRAL', 'SAUDI EASTERN', 'SAUDI JEDDAH', 'SOUTH AFRICA'
    ]
    isc_values = ['BANGLADESH', 'NEPAL', 'PAKISTAN-LAHORE', 'PAKISTAN-KARACHI', 'MALDIVES-GAN', 'MALDIVES-MALE']
    
    # Assign Region based on 'POINT OF SALE' values
    df['Region'] = None
    df.loc[df['POINT OF SALE'].isin(far_east_values), 'Region'] = 'FAR EAST'
    df.loc[df['POINT OF SALE'].isin(europe_values), 'Region'] = 'EUROPE'
    df.loc[df['POINT OF SALE'].isin(srilanka_values), 'Region'] = 'SRI LANKA'
    df.loc[df['POINT OF SALE'].isin(india_values), 'Region'] = 'INDIA'
    df.loc[df['POINT OF SALE'].isin(m_east_and_africa_values), 'Region'] = 'M. EAST AND S. AFRICA'
    df.loc[df['POINT OF SALE'].isin(isc_values), 'Region'] = 'ISC'
    
    return df

# Streamlit app
def main():
    st.title("Upload and Process Excel Files")

    # Upload multiple Excel files
    uploaded_files = st.file_uploader("Upload Excel Files", accept_multiple_files=True, type=["xlsx"])

    if uploaded_files:
        combined_data = None
        reference_columns = [
            'POINT OF SALE', 'CCY', 'ACT -LC', ' TGT-LC', 'VAR %-LC (ACT vsTGT)',
            'LYR-LC (2023/24)', 'VAR %-LC (ACT vs LYR)', 'ACT -USD', ' TGT-USD',
            'VAR %-USD (ACT vsTGT)', 'LYR-USD (2023/24)', 'VAR %-USD (ACT vs LYR)',
            'Act. Using-Bgt. ex. Rates', 'Exchange - gain/( loss)',
            'Act. Using- LY. Ex. Rates', 'Exchange  -gain/(loss)',
            'REVENUE CONT. % - Actual', 'REVENUE CONT. %-LYR'
        ]

        for i, file in enumerate(uploaded_files):
            # Select month for each file
            month = st.selectbox(f"Select the Month for {file.name}", [
                "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
            ])

            st.write(f"Processing file: {file.name}")
            
            # Process each file
            df = process_excel(file, columns_reference=reference_columns, month=month)

            # Assign region to the dataset
            df = assign_region(df)

            # Combine datasets
            if combined_data is None:
                combined_data = df
            else:
                combined_data = pd.concat([combined_data, df], axis=0)

        # Drop unnecessary columns
        columns_to_drop = [
            'CCY', 'ACT -LC', ' TGT-LC', 'VAR %-LC (ACT vsTGT)',
            'LYR-LC (2023/24)', 'VAR %-LC (ACT vs LYR)'
        ]
        combined_data.drop(columns=columns_to_drop, errors='ignore', inplace=True)

        # Drop rows with missing values
        combined_data.dropna(inplace=True)

        # Display the combined dataset
        st.write("Combined Dataset:", combined_data)

        # Option to download the dataset
        csv = combined_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Combined Dataset as CSV",
            data=csv,
            file_name="combined_dataset.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
