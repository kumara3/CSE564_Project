'''
Created on Dec 27 , 2014
Implementation of De Bruijn Graph
@author: kumara3

This script is an implementation of De Bruijn graph used to assemble DNA
fragments called reads. Input : User string and an integer K. K is defined as
the seed length.
Output : Statistics information about  graph

'''
from sys import argv
import os

script,user_string,argv2= argv
k=int(argv2)

# This function gives different k-mers from an input read which is a sequence of string.

def extract_kmers(user_string,k):
   # dict_adj_matrix = {}
    dict_adj_matrix_left = {}
    dict_adj_matrix_right = {}
    kmer_generated=[]
    for i in xrange(0,len(user_string)-(k-1)):
        kmer = user_string[i:i+k]
        kmer_left = user_string[i:i+k-1]
        kmer_right = user_string[i+1:i+k]
        dict_adj_matrix_left.setdefault(kmer_left,{})[kmer_right] = kmer
        dict_adj_matrix_right.setdefault(kmer_right,{})[kmer_left] = kmer
        kmer_generated.append(kmer)
    print "********************STATISTICS GENERATED*************************************"
    print "The Total Number of Nodes generated in De Bruijn Graph is",len(dict_adj_matrix_left)+len(dict_adj_matrix_right)
    print "All the k-mer generated from user input string is ",kmer_generated
    return (dict_adj_matrix_left,dict_adj_matrix_right)
#       Number of nodes is the length of dict_adj_matrix_left and
#       dict_adj_matrix_right

# This function finds different status of nodes in terms of indegree and outdegree.
def Eulerian_status(dict_adj_matrix_copy_left, dict_adj_matrix_copy_right):
    outdegree={}
    indegree = {}
    start_outdegree = {} ## Dictionary to caputure from where the path traversal
    #will begin
    for left_node in dict_adj_matrix_copy_left.keys():
        for right_node in dict_adj_matrix_copy_right.keys():
            if left_node==right_node:
                if len(dict_adj_matrix_copy_left[left_node])==len(dict_adj_matrix_copy_right[right_node]):
                    outdegree[right_node] = 1 # Node is balanced.Number 1 is
                    #pointer showing this
                    indegree[right_node] = 1
                else:
                    outdegree[right_node] = 2 # Node is not balanced. Pointer 2
                    #specifies that
                    indegree[right_node] = 2
        
            if len(dict_adj_matrix_copy_left[left_node])>1: 
                 start_outdegree[left_node] = 3  
    
    for i,j in indegree.iteritems():
        if j==1:
            print "Balanced nodes in the graph are",i
    for k,m in indegree.iteritems():
        if m==2:
            print "Node(s) whose indegree#outdegree in the graph is/are",k


    return start_outdegree


def helper_function(dict_adj_matrix_new_left):
    nodes_visit = []
    edges_visit=[]
    get_nested_keys=[]
    visited_node,visited_edge = None,None
    for each in dict_adj_matrix_new_left.keys():
        for k,v in dict_adj_matrix_new_left[each].iteritems():
            if len(dict_adj_matrix_new_left[each])>1:
                start_node = each
                get_nested_keys.append(k)
                visited_node = get_nested_keys.pop()
                visited_edge = dict_adj_matrix_new_left[each][visited_node]
                nodes_visit.append(visited_node)
                edges_visit.append(visited_edge)
    return (nodes_visit,edges_visit)

# This function walks through the nodes and edges following an eulerian path.
def path_walk(degree,dict_adj_matrix_copy_left):
    final_node_visit,final_edge_visit = [],[]
    visit_balanced_node = []
    visit_balanced_edges = []
    dict_adj_matrix_new_copy=dict_adj_matrix_copy_left.copy()
    helper_function(dict_adj_matrix_copy_left)
    for each_node in dict_adj_matrix_copy_left:
        if len(dict_adj_matrix_copy_left[each_node])==1:
            for k,v in dict_adj_matrix_copy_left[each_node].iteritems():
                visit_balanced_node.append(k)
                visit_balanced_edges.append(v)
        else:
                
            NV,EV=helper_function(dict_adj_matrix_copy_left)
    final_node_visit = visit_balanced_node+NV
    final_edge_visit = visit_balanced_edges+EV
    print "The path covers these nodes",final_node_visit
    print "The path covers these edges only once, following Eulerian path",final_edge_visit


#dict_adj_matrix_new_left,dict_adj_matrix_new_right = extract_kmers('00011101',3)
dict_adj_matrix_new_left,dict_adj_matrix_new_right = extract_kmers(user_string,k)
degree = Eulerian_status(dict_adj_matrix_new_left,dict_adj_matrix_new_right)
print path_walk(degree,dict_adj_matrix_new_left)

