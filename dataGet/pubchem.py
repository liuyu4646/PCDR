import requests
import csv


def read_from_csv(file_path:str, column_names: list) :
    smiles = []
    drugs = []
    dns = []
    nfds = []
    tmouts = []
    index = 0
    count = 1
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
    with open(file_path, "r") as wf:
        reader = csv.DictReader(wf, fieldnames=column_names)

        for row in reader:
            data = dict(row)
            if data["DRUG_NAME"] == "DRUG_NAME":
                continue
            if data["DRUG_NAME"] in dns:
                continue
            else:
                count = count + 1
                dns.append(data["DRUG_NAME"])
            drug = {}
            drug["DRUG_NAME"] = data["DRUG_NAME"]
            drug["DRUG_ID"] = index
            print(drug["DRUG_NAME"])
            rqstr = url + data["DRUG_NAME"] + "/json"
            try:
                 js = requests.post(rqstr,timeout=120)
                 if js.status_code == 200:
                    print("get!")
                    drug["SMILE"] = js.json()["PC_Compounds"][0]["props"][-4]["value"]["sval"]
                    smiles.append(drug["SMILE"])
                    drugs.append(drug)
                    index = index + 1
                 else:
                    print("not found")
                    nfds.append(drug["DRUG_NAME"])
            except requests.exceptions.RequestException as e:
                print(e)
                tmouts.append(drug["DRUG_NAME"])
            #     print('没有跳过这条输出')
            # print('跳过了输出')


        print(count)
    while len(tmouts) > 0:
        for tmout in tmouts:
            drug = {}
            drug["DRUG_NAME"] = tmout
            drug["DRUG_ID"] = index
            rqstr = url + tmout + "/json"
            try:
                js = requests.post(rqstr, timeout=120)
                if js.status_code == 200:
                    print("get!")
                    drug["SMILE"] = js.json()["PC_Compounds"][0]["props"][-4]["value"]["sval"]
                    smiles.append(drug["SMILE"])
                    drugs.append(drug)
                    index = index + 1
                    tmouts.remove(tmout)
                else:
                    print("not found")
                    nfds.append(drug["DRUG_NAME"])
                    tmouts.remove(tmout)
            except requests.exceptions.RequestException as e:
                print(e)
                # tmouts.append(drug["DRUG_NAME"])


    print(nfds)
    return smiles, drugs

def write_to_csv_all(output_path:str,file_columns:list,datas:list):
    with open(output_path,"w", newline="") as wf:
        writer = csv.DictWriter(wf, file_columns)
        writer.writeheader()
        writer.writerows(datas)

def write_to_smi(output_path:str, smiles:list):
    with open(output_path, "w", newline="") as wf:
        writer = wf.writelines(smiles)

if __name__ == '__main__':
    input_file = "./dataInput/GDSC1_fitted_dose_response_25Feb20.csv"
    input_titles = ["DATASET", "NLME_RESULT_ID", "NLME_CURVE_ID", "COSMIC_ID", "CELL_LINE_NAME", "SANGER_MODEL_ID",
                "TCGA_DESC", "DRUG_ID", "DRUG_NAME", "PUTATIVE_TARGET", "PATHWAY_NAME", "COMPANY_ID", "WEBRELEASE",
                "MIN_CONC", "MAX_CONC", "LN_IC50", "AUC", "RMSE", "Z_SCORE"]
    smiles, drugs = read_from_csv(input_file, input_titles)
    output_drugs_file = "./dataOutput/pubchem/pubchem2.csv"
    output_smiles_file = "./dataOutput/pubchem/smiles.smi"
    output_titles = ["DRUG_NAME", "DRUG_ID", "SMILE"]

    write_to_csv_all(output_drugs_file, output_titles,drugs)
    write_to_smi(output_smiles_file,smiles)

