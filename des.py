"""
DES加密（未写解密部分）
@Copyright Copyright (c) 2006
@author Guapo
@see DESCore

@last-update(fatal) 2023-01-07
"""


def strEnc(data, firstKey, secondKey, thirdKey):
    encData = ''
    leng = len(data)
    if firstKey != None and firstKey != '':
        firstKeyBt = getKeyBytes(firstKey)
        firstLength = len(firstKeyBt)
    if secondKey != None and secondKey != '':
        secondKeyBt = getKeyBytes(secondKey)
        secondLength = len(secondKeyBt)
    if thirdKey != None and thirdKey != '':
        thirdKeyBt = getKeyBytes(thirdKey)
        thirdLength = len(thirdKeyBt)

    if leng > 0:
        if leng < 4:
            bt = strToBt(data)
            if firstKey != None and firstKey != '' and secondKey != None and secondKey != '' and thirdKey != None and thirdKey != '':
                tempBt = bt
                for x in range(firstLength):
                    tempBt = enc(tempBt, firstKeyBt[x])
                for y in range(secondLength):
                    tempBt = enc(tempBt, secondKeyBt[y])
                for z in range(thirdLength):
                    tempBt = enc(tempBt, thirdKeyBt[z])
                encByte = tempBt
            else:
                if firstKey != None and firstKey != '' and secondKey != None and secondKey != '':
                    tempBt = bt
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    for y in range(secondLength):
                        tempBt = enc(tempBt, secondKeyBt[y])
                    encByte = tempBt
                else:
                    if firstKey != None and firstKey !="":
                        tempBt = bt
                        for x in range(firstLength):
                            tempBt = enc(tempBt, firstKeyBt[x])
                        encByte = tempBt
            encData = bt64ToHex(encByte)
        else:
            iterator = int(leng/4)
            remainder = leng % 4
            for i in range(iterator):
                tempData = data[i*4+0: i*4+4]
                tempByte = strToBt(tempData)
                if firstKey != None and firstKey != '' and secondKey != None and secondKey != '' and thirdKey != None and thirdKey != '':
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    for y in range(secondLength):
                        tempBt = enc(tempBt, secondKeyBt[y])
                    for z in range(thirdLength):
                        tempBt = enc(tempBt, thirdKeyBt[z])
                    encByte = tempBt
                else:
                    if firstKey != None and firstKey != '' and secondKey != None and secondKey != '':
                        tempBt = tempByte
                        for x in range(firstLength):
                            tempBt = enc(tempBt, firstKeyBt[x])
                        for y in range(secondLength):
                            tempBt = enc(tempBt, secondKeyBt[y])
                        encByte = tempBt
                    else:
                        if firstKey != None and firstKey != "":
                            tempBt = tempByte
                            for x in range(firstLength):
                                tempBt = enc(tempBt, firstKeyBt[x])
                            encByte = tempBt
                encData += bt64ToHex(encByte)
            if remainder > 0:
                remainderData = data[iterator*4+0: leng]
                tempByte = strToBt(remainderData)
                if firstKey != None and firstKey != '' and secondKey != None and secondKey != '' and thirdKey != None and thirdKey != '':
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    for y in range(secondLength):
                        tempBt = enc(tempBt, secondKeyBt[y])
                    for z in range(thirdLength):
                        tempBt = enc(tempBt, thirdKeyBt[z])
                    encByte = tempBt
                else:
                    if firstKey != None and firstKey != '' and secondKey != None and secondKey != '':
                        tempBt = tempByte
                        for x in range(firstLength):
                            tempBt = enc(tempBt, firstKeyBt[x])
                        for y in range(secondLength):
                            tempBt = enc(tempBt, secondKeyBt[y])
                        encByte = tempBt
                    else:
                        if firstKey != None and firstKey != "":
                            tempBt = tempByte
                            for x in range(firstLength):
                                tempBt = enc(tempBt, firstKeyBt[x])
                            encByte = tempBt
                encData += bt64ToHex(encByte)
    return encData


def bt64ToHex(byteData):
    hexx = ''
    for i in range(16):
        bt = ''
        for j in range(4):
            bt += str(byteData[i*4+j])
        hexx += str(bt4ToHex(bt))
    return hexx


def bt4ToHex(binary: str):
    return hex(eval('0b'+binary))[2:].upper()


def getKeyBytes(key: str):
    leng = len(key)
    iterator = int(leng / 4)
    remainder = leng % 4
    keyBytes = [None] * (iterator+1)
    for i in range(iterator):
        keyBytes[i] = strToBt(key[i*4+0: i*4+4])
    if remainder > 0:
        i = iterator
        keyBytes[i] = strToBt(key[i*4+0: leng])
    return keyBytes


def strToBt(strr):
    leng = len(strr)
    bt = [None] * 64  # 调用此函数的程序是否会访问到 None（是否返回存在 None 的 list）
    if leng < 4:
        for i in range(leng):
            k = charCodeAt(strr, i)
            for j in range(16):
                poww = 1
                for m in range(15, j, -1):
                    poww *= 2
                bt[16 * i + j] = int(k / poww) % 2
        for p in range(leng, 4):
            k = 0
            for q in range(16):
                poww = 1
                for m in range(15, q, -1):
                    poww *= 2
                bt[16 * p + q] = int(k / poww) % 2
    else:
        for i in range(4):
            k = charCodeAt(strr, i)
            for j in range(16):
                poww = 1
                for m in range(15, j, -1):
                    poww *= 2
                bt[16 * i + j] = int(k / poww) % 2  # !!!
    return bt


def charCodeAt(strr, i):
    return ord(strr[i])


def enc(dataByte, keyByte):
    keys = generateKeys(keyByte)
    ipByte = initPermute(dataByte)
    ipLeft = [None]*32
    ipRight = [None]*32
    tempLeft = [None]*32
    i, j, k, m, n = 0, 0, 0, 0, 0
    for k in range(32):
        ipLeft[k] = ipByte[k]
        ipRight[k] = ipByte[32 + k]
    for i in range(16):
        for j in range(32):
            tempLeft[j] = ipLeft[j]
            ipLeft[j] = ipRight[j]
        key = [None]*48
        for m in range(48):
            key[m] = keys[i][m]
        tempRight = xor(pPermute(sBoxPermute(xor(expandPermute(ipRight), key))), tempLeft)
        for n in range(32):
            ipRight[n] = tempRight[n]

    finalData = [None]*64
    for i in range(32):
        finalData[i] = ipRight[i]
        finalData[32 + i] = ipLeft[i]
    return finallyPermute(finalData)


def generateKeys(keyByte):
    key = [None]*56
    keys = [[None] * 48 for _ in range(16)]
    loop = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    for i in range(7):
        for j, k in zip(range(8), range(7, -1, -1)):
            key[i*8 + j] = keyByte[8*k + i]
    for i in range(16):
        tempLeft = 0
        tempRight = 0
        for j in range(loop[i]):
            tempLeft = key[0]
            tempRight = key[28]
            for k in range(27):
                key[k] = key[k+1]
                key[28+k] = key[29+k]
            key[27] = tempLeft
            key[55] = tempRight
        tempKey = [None]*48
        temp2key = [13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47, 43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31]
        for index in range(48):
            tempKey[index] = key[temp2key[index]]
        if i in range(16):
            for m in range(48):
                keys[i][m] = tempKey[m]
    return keys


def initPermute(originalData):
    ipByte = [None]*64
    for i, m, n in zip(range(4), range(1, 100, 2), range(0, 100, 2)):
        for j, k in zip(range(7, -1, -1), range(100)):
            ipByte[i*8+k] = originalData[j*8+m]
            ipByte[i*8+k+32] = originalData[j*8+n]
    return ipByte


def xor(byteOne, byteTwo):
    xorByte = [None]*len(byteOne)
    for i in range(len(byteOne)):
        xorByte[i] = byteOne[i] ^ byteTwo[i]
    return xorByte


def pPermute(sBoxByte):
    pBoxPermute = [None]*32
    per2box = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
    for i in range(32):
        pBoxPermute[i] = sBoxByte[per2box[i]]
    return pBoxPermute

def sBoxPermute(expandByte):
    sBoxByte = [None]*32
    s1 = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ]
    s2 = [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ]
    s3 = [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ]
    s4 = [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ]
    s5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ]
    s6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ]
    s7 = [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ]
    s8 = [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
    s_list = [s1, s2, s3, s4, s5, s6, s7, s8]

    for m in range(8):
        i = expandByte[m * 6 + 0] * 2 + expandByte[m * 6 + 5]
        j = expandByte[m * 6 + 1] * 2 * 2 * 2 + expandByte[m * 6 + 2] * 2 * 2 + expandByte[m * 6 + 3] * 2 + expandByte[m * 6 + 4]

        binary = getBoxBinary(s_list[m][i][j])

        sBoxByte[m * 4 + 0] = int(binary[0:1])
        sBoxByte[m * 4 + 1] = int(binary[1:2])
        sBoxByte[m * 4 + 2] = int(binary[2:3])
        sBoxByte[m * 4 + 3] = int(binary[3:4])

    return sBoxByte


def getBoxBinary(i: int):
    binary = str(bin(i))[2:]
    return (4 - len(binary)) * '0' + binary


def expandPermute(rightData):
    epByte = [None]*48
    for i in range(8):
        if i == 0:
            epByte[i * 6 + 0] = rightData[31]
        else:
            epByte[i * 6 + 0] = rightData[i * 4 - 1]
        epByte[i * 6 + 1] = rightData[i * 4 + 0]
        epByte[i * 6 + 2] = rightData[i * 4 + 1]
        epByte[i * 6 + 3] = rightData[i * 4 + 2]
        epByte[i * 6 + 4] = rightData[i * 4 + 3]
        if i == 7:
            epByte[i * 6 + 5] = rightData[0]
        else:
            epByte[i * 6 + 5] = rightData[i * 4 + 4]
    return epByte


def finallyPermute(endByte):
    fpByte = [None]*64
    fp2end = [39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25, 32, 0, 40, 8, 48, 16, 56, 24]
    for i in range(64):
        fpByte[i] = endByte[fp2end[i]]
    return fpByte