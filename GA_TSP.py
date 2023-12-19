import random as rd
import copy as copy
from matplotlib import pyplot as plt

class Location:
    def __init__(self,name,x,y):
        self.name=name
        self.loc=(x,y)
        
    def distance_between(self,location2):
        assert isinstance(location2,Location)
        return ((self.loc[0]-location2.loc[0])**2+(self.loc[1]-location2.loc[1])**2)**(1/2)
def create_locations():
    locations=[]
    xs=[8,50,18,35,90,40,84,74,34,40,60]
    ys=[3,62,0,25,89,71,7,29,45,65,69]
    cities=['P','A','K','O','Y','N','X','G','Q','S','J']
    for x,y,name in zip(xs,ys,cities):
        locations.append(Location(name,x,y))
    return locations,xs,ys,cities

class Route:
    def __init__(self,path):
        self.path=path
        self.length=self._set_length()
    def _set_length(self):
        total_length=0
        path_copy=self.path[:]
        from_here=path_copy.pop(0)
        init_node=copy.deepcopy(from_here)
        
        while path_copy:
            to_there=path_copy.pop(0)
            total_length+=to_there.distance_between(from_here)
            from_here=copy.deepcopy(to_there)
        total_length+=from_here.distance_between(init_node)
        return total_length
class GeneticAlgo:
    def __init__(self, locs, level=100,populations=100,variant=3,mutate_percent=0.1,elite_save_percent=0.2):
        self.locs=locs
        self.level=level
        self.variant=variant
        self.populations=populations
        self.mutates=int(populations*mutate_percent)
        self.elite=int(populations*elite_save_percent)
    def _find_path(self):
        locs_copy=self.locs[:]
        path=[]
        while locs_copy:
            to_there=locs_copy.pop(locs_copy.index(rd.choice(locs_copy)))
            path.append(to_there)
        return path
    def _init_routes(self):
        routes=[]
        for _ in range(self.populations):
            path=self._find_path()
            routes.append(Route(path))
        return routes
    def _get_next_route(self,routes):
        routes.sort(key=lambda x:x.length,reverse=False)
        elites=routes[:self.elite][:]
        crossovers=self._crossover(elites)
        return crossovers[:]+elites
    def _crossover(self,elites):
        normal_breeds=[]
        mutate_ones=[]
        x=0
        for x in range(self.populations-self.mutates):
            father,mother=rd.choices(elites[:4],k=2)
            
            index_start=rd.randrange(0,len(father.path)-self.variant-1)
            father_gene=father.path[index_start:index_start+self.variant]
            father_gene_names=[loc.name for loc in father_gene]
            
            mother_gene=[gene for gene in mother.path if gene.name not in father_gene_names]
            mother_gene_cut=rd.randrange(1,len(mother_gene))
            next_route_path=mother_gene[:mother_gene_cut]+father_gene+mother_gene[mother_gene_cut:]
            next_route=Route(next_route_path)
            normal_breeds.append(next_route)
            
            copy_father=copy.deepcopy(father)
            idx=range(len(copy_father.path))
            gene1,gene2=rd.sample(idx,2)
            copy_father.path[gene1],copy_father.path[gene2]=copy_father.path[gene2],copy_father.path[gene1]
            mutate_ones.append(copy_father)
        mutate_breeds=rd.choices(mutate_ones,k=self.mutates)
        return normal_breeds+mutate_breeds
    def evolution(self):
        x=0
        routes=self._init_routes()
        for x in range(self.level):
            routes=self._get_next_route(routes)
        routes.sort(key=lambda x:x.length)
        return routes[0].path, routes[0].length
if __name__=='__main__':
    my_locs,xs,ys,cities=create_locations()
    my_algo=GeneticAlgo(my_locs,level=40,populations=150,variant=2,mutate_percent=0.02,elite_save_percent=0.2)
    best_route, best_route_length=my_algo.evolution()
    best_route.append(best_route[0])
    print("Best City:",[loc.name for loc in best_route])
    print("Best Loc:",[(loc.loc[0],loc.loc[1]) for loc in best_route])
    print("best_route_length:",best_route_length)
    
    fig,ax=plt.subplots()
    ax.plot([loc.loc[0] for loc in best_route],[loc.loc[1] for loc in best_route],'red',linestyle='-',marker='')
    ax.scatter(xs,ys)
    for i,txt in enumerate(cities):
        ax.annotate(txt,(xs[i],ys[i]))
    plt.show()