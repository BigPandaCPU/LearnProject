from bpa import BPA

# bpa = BPA(path='./data/bunny_with_normals.txt', radius=0.01, visualizer=True)
# bpa.create_mesh(limit_iterations=10000)

from bpa import BPA

bpa = BPA(path='./data/bunny_with_normals.txt', radius=0.005, visualizer=True)
bpa.visualizer.draw_with_normals(percentage=80, normals_size=0.01)