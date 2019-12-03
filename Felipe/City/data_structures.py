class Point:
    def __init__(self,x = 0.0, y = 0.0): 
        self.x = x 
        self.y = y
    pass

class Rectangle:
    def __init__(self,p = Point(0.0, 0.0), w = 1,0, h = 1.0): 
        self.p = p
        self.w = w
        self.h = h
    
    def is_point_inside(point):
        return ((self.p.x < point.x and point.x < (self.p.x + self.w)) and 
                (self.p.y < point.y and point.y < (self.p.y + self.h)))
    
    def is_colliding(rect):
        p0 = rect.p
        p1 = Point(p0.x + rect.w, p0.y)
        p2 = Point(p0.x, p0.y + rect.h)
        p3 = Point(p0.x + rect.w, p0.y + rect.h)
        
        return (is_point_inside(p0) or is_point_inside(p1) or
                is_point_inside(p2) or is_point_inside(p3))

    pass

