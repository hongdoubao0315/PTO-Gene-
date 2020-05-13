'''
将PTO与gene进行比对，找出同一篇文献PTO与gene共显性
PTO文件：match_result.txt
gene文件：gene.txt
输出文件：match.txt
'''

f1 = open('/Users/apple/Downloads/PTO and Gene/match/gene.txt',encoding="utf-8")
f2 = open('/Users/apple/Downloads/PTO and Gene/match/sort_match_PTO.txt',encoding="utf-8")
wf = open('/Users/apple/Downloads/PTO and Gene/match/match.txt', 'w')
wf2 = open('/Users/apple/Downloads/PTO and Gene/match/match2.txt', 'w')

f1_list = f1.readlines()
f2_list = f2.readlines()
f1.close()
f2.close()
wf.write('PMID\tgene_id\tgene_name\tgene_time\tPTO\tterm\tPTO_time\n')
wf2.write('(gene_id,PTO)\ttime\n')

count_a = 0
count_b = 0
gene_to_dic = {}
for line in f1_list:
    l = line.strip()
    line1 = l.split('\t')
    if line1[0] != 'PMID':
        for i in f2_list:
            l2 = i.strip()
            line2 = l2.split('\t')
            if line1[0] == line2[0]:
                gene_to_dic[(line1[1],line2[1])] = 0

for line in f1_list:  #遍历pubtator中挖掘的gene
    l = line.strip()
    line1 = l.split('\t')
    count_a += 1
    if line1[0] != 'PMID': #跳过标题行
        PMID = line1[0]
        gene_id = line1[1]
        gene_time = line1[2]
        gene_name = line1[3]
        for i in f2_list:  #遍历reference中挖掘的PTO
            l2 = i.strip()
            line2 = l2.split('\t')
            if line2[0] != 'pmid':  #跳过标题行
                PMID_2 = line2[0]
                if PMID_2 == PMID:  #如果pmid匹配成功
                    gene_to_dic[(line1[1],line2[1])] += 1
                    count_b += 1
                    PTO = line2[1]
                    term = line2[2]
                    PTO_time = line2[3]
                    wf.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.\
                             format(PMID,gene_id,gene_name,gene_time,PTO,term,PTO_time))
    if count_a % 100 == 0:  #输出了多次？？
        print('{0}/{1} has been done.'.format(count_a, len(f1_list)))
#print(count_b)
for i in gene_to_dic:
    time = gene_to_dic[i]
    wf2.write('{0}\t{1}\n'.format(i,time))
        

wf.close()
wf2.close()