def transformarEmBits(memoria):
    if "bits" in memoria:
        return int(memoria.split('bits')[0])
    elif "KB" in memoria:
        return int(memoria.split('KB')[0])*1024*8
    elif "MB" in memoria:
        return int(memoria.split('MB')[0])*1024*1024*8
    elif "GB" in memoria:
        return int(memoria.split('GB')[0])*1024*1024*1024*8
    elif "TB" in memoria:
        return int(memoria.split('TB')[0])*1024*1024*1024*1024*8
    elif "B" in memoria:
        return int(memoria.split('B')[0])*8
    else:
        print("Unidade de memória inserida não suportada. Unidades aceitas: bits, B, KB, MB, GB, TB")