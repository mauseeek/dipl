def Battery_select(brand, file, *soc):

    if brand not in ["LG", "S"]:
        raise ValueError("Wrong File Type argument")

    # ******* MEASUREMENT files ********

    Measurement_files = {
        "LG": {
            "10": "PulseTest_LG02_SOC_10",
            "30": "PulseTest_LG02_SOC_30",
            "50": "PulseTest_LG02_SOC_50",
            "70": "PulseTest_LG02_SOC_70",
            "90": "PulseTest_LG02_SOC_90"},
        "S": {
            "10": "Pulzno_10SOC",
            "30": "Pulzno_30SOC",
            "50": "Pulzno_50SOC",
            "70": "Pulzno_70SOC",
            "90": "Pulzno_90SOC"}
    }

    # ******* OCV files ****************

    OCV_files = {"LG": "OCV_Average_LG18650",
                 "S": "OCV_Average_Samsung18650"}

    # ******* HYSTERESIS files ********

    Hysteresis_files = {"LG": "U_H_LG18650",
                        "S": "U_H0_Samsung18650"}

    # **********************************

    if file == "Measurement":
        return Measurement_files[brand][soc[0]]

    elif file == "OCV":
        return OCV_files[brand]

    elif file == "Hysteresis":
        return Hysteresis_files[brand]

    else:
        raise ValueError("Wrong File Type argument")


def Print_optimal(opt_params, beta_fitting, U_H0_fitting, prefix):
    #  Assuming opt_params is a list or tuple containing the optimized parameters
    num_params = len(opt_params)

    # Print the optimal parameters based on their availability
    print(prefix, "Optimal R0 =", opt_params[0])
    print(prefix, "Optimal R1 =", opt_params[1])
    print(prefix, "Optimal C1 =", opt_params[2])
    print(prefix, "Optimal R2 =", opt_params[3])
    print(prefix, "Optimal C2 =", opt_params[4])

    # Check for beta and U_H0 based on fitting flags and number of parameters
    if beta_fitting[0] == "1":
        print(prefix, "Optimal beta =", opt_params[5])
    if U_H0_fitting[0] == "1":
        print(prefix, "Optimal U_H0 =", opt_params[6])

    if len(opt_params) - 5 > int(beta_fitting[0] == "1") + int(U_H0_fitting == "1"):
        print(prefix, "Optimal SOC_init =", opt_params[-1])

    return


def Plot_compare(U_B_optimized, U_B_measured_for_comparison, time_simulated, Hysteresis_enable, beta_fitting, U_H0_fitting, brand, soc_value, str_SOC, suffix):
    import matplotlib.pyplot as plt

    if Hysteresis_enable == "1":
        str_beta = ", Beta Fitting" if beta_fitting[0] == "1" else ", Beta Fixed"
        str_U_H0 = ", U_H0 Fitting" if U_H0_fitting[0] == "1" else ", U_H0 Fixed" if U_H0_fitting[0] == "0" else ", U_H0 Measured"
        str_hys = "With Hysteresis"
    else:
        str_beta = str_U_H0 = ""
        str_hys = "Without Hysteresis"

    plt.figure().set_figwidth(10)
    plt.plot(time_simulated, U_B_optimized, color="limegreen", linewidth=3, label="simulated - optimal")
    plt.plot(time_simulated, U_B_measured_for_comparison, color="blue", linewidth=3, label="measured")
    plt.title("Simulation results " + brand + " " + soc_value + " SOC - " + str_hys + suffix + "\n(optimization Rx, Cx" + str_SOC + str_beta + str_U_H0 + ")")
    plt.xlabel("time [s]")
    plt.ylabel("Voltage [V]")
    plt.grid(True)
    plt.legend()
    plt.show()

    return
