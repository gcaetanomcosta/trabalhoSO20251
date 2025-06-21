def transformarEmBytes(memoria):
    if "KB" in memoria:
        return int(memoria.split('KB')[0])*1024
    elif "MB" in memoria:
        return int(memoria.split('MB')[0])*1024*1024
    elif "GB" in memoria:
        return int(memoria.split('GB')[0])*1024*1024*1024
    elif "TB" in memoria:
        return int(memoria.split('TB')[0])*1024*1024*1024*1024
    elif "B" in memoria:
        return int(memoria.split('B')[0])
    else:
        print("Unidade de memória inserida não suportada. Unidades aceitas: bits, B, KB, MB, GB, TB")