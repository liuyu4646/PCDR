import csv
def write_to_tsv(output_path: str, file_columns: list, data: list):
    csv.register_dialect('tsv_dialect', delimiter='\t', quoting=csv.QUOTE_ALL)
    with open(output_path, "w", newline="") as wf:
        writer = csv.DictWriter(wf, fieldnames=file_columns, dialect='tsv_dialect')
        writer.writerows(data)
    csv.unregister_dialect('tsv_dialect')

def write_to_csv_all(output_path:str,file_columns:list,datas:list):
    with open(output_path,"w", newline="") as wf:
        writer = csv.DictWriter(wf, file_columns)
        writer.writeheader()
        writer.writerows(datas)
def read_from_csv(file_path:str, column_names: list) -> list:
    cln = []
    with open(file_path, "r") as wf:
        reader = csv.DictReader(wf, fieldnames=column_names)
        for row in reader:
            data = dict(row)
            if data["CELL_LINE_NAME"] not in cln:
                cln.append(data["CELL_LINE_NAME"])
    print(len(cln))
    return cln
def read_from_tsv(file_path: str, column_names: list, cln: list) :
    # file_path:path of file of input
    # column_names: list of keys of input file
    # cln:list of keys of output file
    print(cln)
    csv.register_dialect('tsv_dialect', delimiter='\t', quoting=csv.QUOTE_ALL)
    titles = ["CELL_LINE"]
    samples = []
    contents = []
    index = 0
    flag = 1
    with open(file_path, "r") as wf:
        reader = csv.DictReader(wf, fieldnames=column_names, dialect='tsv_dialect')
        # datas = []
        for row in reader:
            data = dict(row)
            # datas.append(data)
            if data["GENE_NAME"] == "GENE_NAME":
                continue
            if data["SAMPLE_NAME"] not in cln:
                index = index + 1
                if index >= 1000000:
                    print(index * flag)
                    index = 0
                    flag = flag + 1
                continue
            # print(data["SAMPLE_NAME"])
            if data["GENE_NAME"] not in titles:
                # print("gene:"+data["GENE_NAME"])
                if data["SAMPLE_NAME"] not in samples:
                    print("sample:"+data["SAMPLE_NAME"])
                    samples.append(data["SAMPLE_NAME"])
                    content = {}
                    # for title in titles:
                    #     content[title] = "oops"
                    content["CELL_LINE"] = data["SAMPLE_NAME"]
                    content[data["GENE_NAME"]] = data["Z_SCORE"]
                    contents.append(content)
                else:
                    contents[samples.index(data["SAMPLE_NAME"])][data["GENE_NAME"]] = data["Z_SCORE"]
                titles.append(data["GENE_NAME"])
            else:
                if data["SAMPLE_NAME"] not in samples:
                    samples.append(data["SAMPLE_NAME"])
                    content = {}
                    content["CELL_LINE"] = data["SAMPLE_NAME"]
                    content[data["GENE_NAME"]] = data["Z_SCORE"]
                    contents.append(content)
                else:
                    contents[samples.index(data["SAMPLE_NAME"])][data["GENE_NAME"]] = data["Z_SCORE"]
            index = index+1
            if index >= 10000:
                print(index*flag)
                index = 0
                flag = flag+1
        # print(contents)
        # return contents, titles

    csv.unregister_dialect('tsv_dialect')
    print("cell lines:")
    print(len(cln))
    print("samples:")
    print(len(samples))
    miss = list(set(cln).difference(set(samples)))
    print(miss)
    print("miss:")
    print(len(miss))
    print("titles:")
    print(len(titles))
    if cln == samples:
        print("same")
    else:
        print("not same")
    return contents, titles

def getTitle(datas:list):
    titles = ["CELL_LINE"]
    samples = []
    contents = []
    for data in datas:
        if data["GENE_NAME"]== "GENE_NAME":
            continue
        if data["GENE_NAME"] not in titles:
            # print("gene:"+data["GENE_NAME"])
            if data["SAMPLE_NAME"] not in samples:
                # print("sample:"+data["SAMPLE_NAME"])
                samples.append(data["SAMPLE_NAME"])
                content={}
                # for title in titles:
                #     content[title] = "oops"
                content["CELL_LINE"] = data["SAMPLE_NAME"]
                content[data["GENE_NAME"]] = data["Z_SCORE"]
                contents.append(content)
            else:
                contents[samples.index(data["SAMPLE_NAME"])][data["GENE_NAME"]] = data["Z_SCORE"]
            titles.append(data["GENE_NAME"])
        else:
            if data["SAMPLE_NAME"] not in samples:
                samples.append(data["SAMPLE_NAME"])
                content={}
                content["CELL_LINE"] = data["SAMPLE_NAME"]
                content[data["GENE_NAME"]] = data["Z_SCORE"]
                contents.append(content)
            else:
                contents[samples.index(data["SAMPLE_NAME"])][data["GENE_NAME"]] = data["Z_SCORE"]
    # print(contents)
    return contents, titles


if __name__ == "__main__":
    fn = "./dataInput/CosmicCLP_CompleteGeneExpression.tsv"
    fcln = "./dataInput/GDSC1_fitted_dose_response_25Feb20.csv"
    title = ["SAMPLE_ID",	"SAMPLE_NAME",	"GENE_NAME", "REGULATION",	"Z_SCORE"]
    titlecln = ["DATASET", "NLME_RESULT_ID", "NLME_CURVE_ID", "COSMIC_ID", "CELL_LINE_NAME", "SANGER_MODEL_ID", "TCGA_DESC", "DRUG_ID", "DRUG_NAME", "PUTATIVE_TARGET", "PATHWAY_NAME", "COMPANY_ID", "WEBRELEASE", "MIN_CONC", "MAX_CONC", "LN_IC50", "AUC", "RMSE", "Z_SCORE"]
    cln = read_from_csv(fcln, titlecln)
    # print(len(cln))
    print("start")
    output, titles = read_from_tsv(fn, title, cln)
    # datas=read_from_tsv(fs,titletest)
    # =getTitle(datas)
    # print(titles)
    write_to_csv_all("./dataOutput/gene/geneExpression.csv", titles, output)
