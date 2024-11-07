import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
import matplotlib

# Suppress warnings
warnings.filterwarnings("ignore")

# Set a non-interactive backend for matplotlib
matplotlib.use('Agg')

try:
    # Debug statement to indicate start
    print("Starting script...")

    
    non_optimized = np.array([45, 43, 47, 50, 44, 46, 42, 48, 45, 44])
    optimized = np.array([35, 36, 34, 33, 38, 37, 36, 34, 35, 36])

    # Perform independent t-test
    print("Performing t-test...")
    t_statistic, p_value = stats.ttest_ind(non_optimized, optimized)

    # Visualization: Travel Comparison
    print("Plotting data...")
    plt.figure(figsize=(10, 6))
    plt.plot(non_optimized, 'bo-', label=' Travel Speed Tom Tom', markerfacecolor='blue')
    plt.plot(optimized, 'rs-', label=' Travel Speed (SUMO)', markerfacecolor='red')
    plt.title('Comparison of Speed Times: SUMO vs. Tom Tom')
    plt.xlabel('Sample Index')
    plt.ylabel('Travel Speed (km/h)')
    plt.legend()
    plt.grid(True)
    
    # Save plot instead of showing it
    plt.savefig("travel_speed_comparison.png")
    print("Plot saved as 'travel_speed_comparison.png'")

    # Print the results of the t-test
    print(f"T-statistic: {t_statistic}")
    print(f"P-value: {p_value}")

    # Interpretation based on p-value
    print("Interpreting p-value...")
    alpha = 0.05
    if p_value < alpha:
        print("Reject the null hypothesis: The travel speed are significantly different.")
    else:
        print("Fail to reject the null hypothesis: No significant difference in travel speed.")

    # Debug statement to indicate end
    print("Script completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
