import os
import pandas as pd
from tkinter import Tk, filedialog

# Configure pandas
pd.options.mode.use_inf_as_na = True

# Open folder selection dialog
Tk().withdraw()
folder_path = filedialog.askdirectory(title="Select folder containing CSV files")

# --- Function to load and parse T_ files ---
def load_T_files(folder):
    all_files = os.listdir(folder)
    t_csv_files = [f for f in all_files if f.endswith(".csv") and "T_" in f]
    t_dataframes = []

    for file in t_csv_files:
        try:
            file_path = os.path.join(folder, file)
            df = pd.read_csv(file_path)

            # Skip first 3 rows, get relevant columns
            dist = df.loc[3:, 'TOTAL_DISTANCE_TRAVELED'].astype(float).reset_index(drop=True)
            label = df.loc[3:, 'LABEL'].astype(str).reset_index(drop=True)
            track_id = df.loc[3:, 'TRACK_ID'].astype(int).reset_index(drop=True)

            temp_df = pd.DataFrame({
                'TRACK_ID': track_id,
                'Distance': dist,
                'Label': label,
                'Source': file
            })

            t_dataframes.append(temp_df)

        except Exception as e:
            print(f"Error loading T_ file {file}: {e}")

    return pd.concat(t_dataframes, ignore_index=True)


# --- Function to load and parse S_ files ---
def load_S_files(folder):
    all_files = os.listdir(folder)
    s_csv_files = [f for f in all_files if f.endswith(".csv") and "S_" in f]
    s_dataframes = []

    for file in s_csv_files:
        try:
            file_path = os.path.join(folder, file)
            df = pd.read_csv(file_path, skiprows=[1, 2, 3])

            final_positions = []

            for track_id in df['TRACK_ID'].unique():
                track_data = df[df['TRACK_ID'] == track_id]
                last_frame = track_data['FRAME'].max()
                y_final = track_data.loc[track_data['FRAME'] == last_frame, 'POSITION_Y'].values
                if len(y_final) > 0:
                    final_positions.append((int(track_id), y_final[0]))

            temp_df = pd.DataFrame(final_positions, columns=['TRACK_ID', 'Y'])
            temp_df['Source'] = file
            s_dataframes.append(temp_df)

        except Exception as e:
            print(f"Error loading S_ file {file}: {e}")

    return pd.concat(s_dataframes, ignore_index=True)


# --- Load Data ---
print("Loading T_ files...")
df_T = load_T_files(folder_path)

print("Loading S_ files...")
df_S = load_S_files(folder_path)

# --- Merge and Compute Chemotaxis ---
print("Merging and computing chemotaxis index...")

# Ensure types are correct
df_T['TRACK_ID'] = df_T['TRACK_ID'].astype(int)
df_S['TRACK_ID'] = df_S['TRACK_ID'].astype(int)
# Normalize Source: remove T_ and S_ prefixes
df_T['Source'] = df_T['Source'].str.replace(r'^T_', '', regex=True)
df_S['Source'] = df_S['Source'].str.replace(r'^S_', '', regex=True)
# Merge T and S on TRACK_ID and Source
merged_df = pd.merge(
    df_T,
    df_S,
    on=['TRACK_ID', 'Source'],
    how='inner'
)

# Calculate chemotaxis index
merged_df['Chemotaxis'] = (1100 - merged_df['Y']) / merged_df['Distance']

# --- Save Output ---
output_path = os.path.join(folder_path, 'analysed.csv')
merged_df.to_csv(output_path, index=False)

print(f"✅ Analysis complete. Results saved to:\n{output_path}")

