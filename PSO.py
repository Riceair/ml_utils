import numpy as np
import random

class PSO():
    def __init__(self, fitness, pN, dim, pmax, pmin, max_iter, w=0.8, c1=2, c2=2):
        self.w=w #慣性權重
        self.c1=c1 #速度權重
        self.c2=c2 #速度權重
        self.r1=random.uniform(0, 1) #速度權重
        self.r2=random.uniform(0, 1) #速度權重
        self.pN=pN #粒子數量
        self.dim=dim #粒子維度
        self.pmax = pmax #座標最大值
        self.pmin = pmin #座標最大值
        self.max_iter=max_iter #疊代次數
        self.X=np.zeros((self.pN, self.dim)) #粒子座標
        self.V=np.zeros((self.pN, self.dim)) #粒子速度
        self.pbest=np.zeros((self.pN, self.dim)) #個體最佳位置
        self.gbest=np.zeros((1, self.dim)) #群體最佳位置
        self.p_fit=np.zeros(self.pN) #個體最佳適應值
        self.g_fit=-1e20 #群體最佳適應值
        self.fitness=fitness #適應函數
        self.fit_history=[] #紀錄適應值的歷史
    
    def init_Population(self):
        for i in range(self.pN): #產生pN個粒子
            for j in range(self.dim): #產生粒子每個維度的內容
                self.X[i][j]=random.uniform(self.pmin, self.pmax) #隨機生成座標
                self.V[i][j]=0 #隨機生成速度
            self.pbest[i]=self.X[i]
            tmp=self.fitness(self.X[i])
            self.p_fit[i]=tmp
            if tmp>self.g_fit: #生成群體最佳解
                self.g_fit=tmp
                self.gbest=self.X[i]
                
    def iterator(self):
        self.fit_history=[]
        for _ in range(self.max_iter):
            for i in range(self.pN): #更新gbest/pbest
                temp=self.fitness(self.X[i])
                if temp>self.p_fit[i]: #更新個體最佳
                    self.p_fit[i]=temp
                    self.pbest[i]=self.X[i].copy() #需用複製，因為存的是array
                    if self.p_fit[i]>self.g_fit: #更新群體最佳
                        self.gbest=self.X[i].copy() #需用複製，因為存的是array
                        self.g_fit=self.p_fit[i]
            for i in range(self.pN): #更新所有個體
                self.V[i]=self.w*self.V[i]+self.c1*self.r1*(self.pbest[i]-self.X[i])+\
                          self.c2*self.r2*(self.gbest-self.X[i])
                self.X[i]=self.X[i]+self.V[i]
            self.fit_history.append(self.g_fit) #歷史紀錄
        return self.gbest, self.g_fit

    def getHistory(self):
        return self.fit_history