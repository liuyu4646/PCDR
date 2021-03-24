import csv
import matplotlib.pyplot as plt




missDrugs = ['WZ-1-84', 'JW-7-52-1', 'JQ12', 'TL-2-105', 'Genentech Cpd 10', 'QL-XII-47', 'WZ3105', 'XMD14-99', 'JW-7-24-1', 'NPK76-II-72-1', 'TL-1-85', 'VNLG/124', 'KIN001-236', 'KIN001-244', 'KIN001-042', 'KIN001-260', 'KIN001-266', 'MPS-1-IN-1', 'SB52334', 'QL-XI-92', 'XMD13-2', 'XMD15-27', 'THZ-2-49', 'KIN001-270', 'THZ-2-102-1', 'Brivanib, BMS-540215', 'LIMK1 inhibitor BMS4', 'eEF2K Inhibitor, A-484954', 'MetAP2 Inhibitor, A832234', 'Venotoclax', 'CAP-232, TT-232, TLN-232', 'Cisplatin', 'Nutlin-3a (-)', 'Mirin', 'Cetuximab', 'HG-5-113-01', 'HG-5-88-01', 'XMD11-85h', 'QL-VIII-58', 'QL-XII-61', 'rTRAIL', 'ICL1100013', 'Bleomycin (50 uM)', 'Bleomycin (10 uM)', 'Dyrk1b_0191', 'EphB4_9721', 'FEN1_3940', 'FGFR_0939', 'FGFR_3831', 'AZD7969', 'IAP_5620', 'IAP_7638', 'IGFR_3801', 'JAK1_3715', 'JAK3_7406', 'MCT1_6447', 'MCT4_1422', 'PI3Ka_4409', 'PLK_6522', 'RAF_9304', 'PARP_9495', 'PARP_0108', 'PARP_9482', 'TANK_1366', 'TTK_3146']
missSamples = ['SNU-1', 'NB4', 'KP-N-RT-BM-1', 'NCI-H2818', 'NCI-H3118', 'NCI-H513', 'YMB-1-E', 'NCI-H460', 'NCI-H2081', 'NCI-H128', 'NCI-H2803',  'MHH-ES-1', 'OVCA433', 'SNU-16', 'T24', 'UWB1.289', 'DiFi', 'NCI-H2595', 'NCI-H2373', 'KP-N-YS', 'Hs-746T', 'Hep3B2-1-7', 'NTERA-2-cl-D1', 'NCI-H2810', 'B-CPAP', 'HuTu-80', 'NCI-H2369', 'NCI-H2722', 'NCI-H1437', 'HCC-33', 'TALL-1', 'MDA-MB-175-VII', 'CP67-MEL', 'OMC-1', 'BC-3', 'NCI-H2171', 'NCI-H290', 'Hs-939-T', 'CAPAN-2', 'SC-1', 'MY-M12', 'MMAc-SF', 'HT', 'NCI-H2731', 'NCI-H2795', 'KMH-2', 'SNU-5', 'Hs-683', 'NCI-H2869', 'NK-92MI', 'VMRC-MELG', 'PE-CA-PJ15', 'NCI-H2591', 'TMK-1', 'PC-3_[JPC-3]', 'VMRC-RCW', 'NCI-H2461', 'Hs-940-T', 'MC-IXC', 'NCI-H2804', 'Hs-633T', 'Hs-766T', 'NCI-H508', 'G-292-Clone-A141B1', 'Caov-3']


def deleteMiss(inputPath: str, outputPath: str, titles: list):
    with open(inputPath, 'r') as rf:
        with open(outputPath, "w", newline="") as wf:
            reader = csv.DictReader(rf, fieldnames=titles)
            writer = csv.DictWriter(wf, fieldnames=titles)
            for row in reader:
                data = dict(row)
                if data["CELL_LINE_NAME"]  in  missSamples or data["DRUG_NAME"] in missDrugs:
                    continue
                else:
                    writer.writerow(data)

def showDisplay(inputPath: str, titles: list):
    ic50s = []
    index = 0
    j = 0
    with open(inputPath, "r") as rf:
        reader = csv.DictReader(rf, fieldnames=titles)
        for row in reader:
            data = dict(row)
            j = j + 1
            if data["LN_IC50"] == "LN_IC50":
                continue

            if float(data["LN_IC50"]) < -2:
                index = index +1


            # print(data["LN_IC50"])
            ic50s.append(float(data["LN_IC50"]))
            # print(float(data["LN_IC50"]))

    plt.hist(ic50s, bins=30)
    print(index)
    plt.show()
    print(j)

if __name__ == '__main__':
    inputPath = "./dataInput/GDSC1_fitted_dose_response_25Feb20.csv"
    outputPath = "./dataOutput/IC50/IC50-1.csv"
    input_titles = ["DATASET", "NLME_RESULT_ID", "NLME_CURVE_ID", "COSMIC_ID", "CELL_LINE_NAME", "SANGER_MODEL_ID",
                    "TCGA_DESC", "DRUG_ID", "DRUG_NAME", "PUTATIVE_TARGET", "PATHWAY_NAME", "COMPANY_ID", "WEBRELEASE",
                    "MIN_CONC", "MAX_CONC", "LN_IC50", "AUC", "RMSE", "Z_SCORE"]

    # deleteMiss(inputPath, outputPath, input_titles)

    showDisplay(outputPath, input_titles)

