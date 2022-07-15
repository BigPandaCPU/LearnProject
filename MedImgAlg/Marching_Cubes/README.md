# MarchingCube
参考 http://paulbourke.net/geometry/polygonise/
在该系列算法中，volexample的最好理解，本算法是模仿该算法。
version0.1:
实现marching cubes的基本功能

version0.1:
速度优化：
将原来的 TRIANGLE *tri = NULL;用来记录所有的triangle的指针，vector容器来替代，避免每次都要进行realloc
//TRIANGLE *tri = NULL;
//tri = (TRIANGLE*)realloc(tri, (ntri + n) * sizeof(TRIANGLE)); //这里每次都要realloc，不是很好
//tri[ntri + l] = triangles[l];

替换为
std::vector<TRIANGLE> tri;
tri.push_back(triangles[l]);

速度提升100倍以上。（realloc非常费时）

version0.2：
将补充表面平滑功能

--输入：-i threshold filename
--输出STL：顺手输出.stl模型文件呗，可以拿其他软件查看重建结果
