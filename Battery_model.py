def RC_model(params, sim_time, delta_t, sim_I_L, sim_SOC, OCV_interp, sim_HYS, Hysteresis_enable, beta_fitting, U_H0_fitting):

    import numpy as np

    beta = beta_fitting[1]
    U_H0 = U_H0_fitting[1]

    if len(params) == 7:  # All parameters provided
        R_0, R_pa, C_pa, R_pc, C_pc, beta, U_H0 = params
    elif len(params) == 6:  # One of beta or U_H0 missing
        if beta_fitting[0] == "1":
            R_0, R_pa, C_pa, R_pc, C_pc, beta = params
        if U_H0_fitting[0] == "1":
            R_0, R_pa, C_pa, R_pc, C_pc, U_H0 = params
    elif len(params) == 5:  # Both beta and U_H0 missing
        R_0, R_pa, C_pa, R_pc, C_pc = params

    U_pa = np.zeros(len(sim_time)+1)
    U_pc = np.zeros(len(sim_time)+1)
    U_H  = np.zeros(len(sim_time)+1)

    #TODO ZAČETNI POGOJ
    U_H[0] = np.sign(sim_I_L[0]) * sim_HYS[0]
    #print(U_H[0])

    #Linerised DE - Backward diferentiation scheme
    for i in range(0,len(sim_time)):
        U_pa[i+1] = 1/(1 + (delta_t/(R_pa*C_pa)))*(delta_t*sim_I_L[i]/C_pa + U_pa[i])
        U_pc[i+1] = 1/(1 + (delta_t/(R_pc*C_pc)))*(delta_t*sim_I_L[i]/C_pc + U_pc[i])

        if Hysteresis_enable == "1":

            if U_H0_fitting[0] == ("0" or "1"):
                # With "I"
                U_H[i+1] = (U_H[i] + beta * delta_t * U_H0 * sim_I_L[i])                                 / (1 + beta * delta_t * sim_I_L[i] * np.sign(sim_I_L[i]))
                # W/O  "I"
                # U_H[i+1] = (U_H[i] + beta * delta_t * U_H0 * np.sign(sim_I_L[i]))                      / (1 + beta * delta_t * np.sign(sim_I_L[i]))
            elif U_H0_fitting[0] == "f":
                # With "I" ##################################################################################################################################################
                # U_H[i+1] = (U_H[i] + beta * delta_t * sim_HYS[i] * sim_I_L[i] * np.sign(sim_I_L[i]))  / (1 + beta * delta_t * sim_I_L[i] * np.sign(sim_I_L[i])) # SIGN zunaj
                # U_H[i+1] = (U_H[i] + beta * delta_t * sim_HYS[i] * sim_I_L[i])                        / (1 + beta * delta_t * sim_I_L[i] * np.sign(sim_I_L[i])) # SIGN pri U_H
                # U_H[i+1] = (U_H[i] + beta * delta_t * sim_HYS[i] * sim_I_L[i] * np.sign(sim_I_L[i]))  / (1 + beta * delta_t * sim_I_L[i]) # SIGN pri U_H0

                # W/O "I" ##################################################################################################################################################
                U_H[i+1] = (U_H[i] + beta * delta_t * sim_HYS[i] * np.sign(sim_I_L[i]))                 / (1 + beta * delta_t * np.sign(sim_I_L[i])) # SIGN zunaj
                # U_H[i+1] = (U_H[i] + beta * delta_t * sim_HYS[i])                                     / (1 + beta * delta_t * np.sign(sim_I_L[i])) # SIGN pri U_H
                # U_H[i+1] = (U_H[i] + beta * delta_t * sim_HYS[i] * np.sign(sim_I_L[i]))               / (1 + beta * delta_t) #SIGN pri U_H0

                # TESTING ##################################################################################################################################################
                # U_H[i+1] = np.sign(sim_HYS[i]) * sim_HYS[i]


    #Dodatni dve metodi po katerih lako izračunamo U_pa in U_pc - odkomentiraj, če želiš testirat.
    # Rezultat je za vse tri metode zelo podoben (vsaj do osme decimalke)
    """
    #Linerised DE - Forward diferentiation scheme
    for i in range(0,len(sim_time)):
        U_pa[i+1] = delta_t*sim_I_L[i]/C_pa + (delta_t/(R_pa*C_pa) + 1)*U_pa[i]
        U_pc[i+1] = delta_t*sim_I_L[i]/C_pc + (delta_t/(R_pc*C_pc) + 1)*U_pc[i]

    #analitic (exponential) solution on smal step
    expo = math.exp(-delta_t/(R_pa*C_pa))
    for i in range(0,len(sim_time)):
        U_pa[i+1] = sim_I_L[i]*R_pa + (U_pa[i-1] - sim_I_L[i]*R_pa)*expo
        U_pc[i+1] = sim_I_L[i]*R_pc + (U_pc[i-1] - sim_I_L[i]*R_pc)*expo
    """
    if Hysteresis_enable == "1":
        U_L = OCV_interp(sim_SOC) + U_pa[1:] + U_pc[1:] + sim_I_L*R_0 + U_H[1:]
    else:
        U_L = OCV_interp(sim_SOC) + U_pa[1:] + U_pc[1:] + sim_I_L*R_0
    return U_L
