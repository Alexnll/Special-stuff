// https://www.zhihu.com/question/27917305/answer/46652009
PImage img;
ArrayList <Circle> circles = new ArrayList <Circle> ();
int shiftx, shifty;

void setup(){
  size(480, 480);
  //noLoop();
  colorMode(HSB);
  background(255);
  smooth();
  noStroke();
  img = loadImage("Apple_logo.jpg");
  shiftx = width/2-img.width/2;
  shifty = height/2-img.height/2;
  img.loadPixels();
  //image(img,shiftx,shifty);
}

void draw(){
  //img.loadPixels();
  background(255);
  //image(img,shiftx,shifty);
  if(circles.size()>0){
    for(Circle c : circles){
      c.display();
    }
  }
  float xn, yn;
  while(true){
    xn = (randomGaussian()*200)+mouseX;
    yn = (randomGaussian()*200)+mouseY;
    int xns,yns;
    xns = (int) (xn-shiftx);
    yns = (int) (yn-shifty);
    if (xns<0 || xns>=img.width || yns<0 || yns>=img.height) break;
    int loc = xns + yns*img.width;
    float b=brightness(img.pixels[loc]);
    if(b>50){
      break;
    }
  }
  boolean sign = true;
  for(Circle c:circles){
    if(dist(xn,yn,c.x,c.y)<c.r+2){
      sign = false;
      break;
    }
  }
  if(sign){     
    Circle cir = new Circle(xn,yn);
    cir.grow(randomGaussian()*5+10);
    circles.add(cir);
  }
}


class Circle{
  float x,y,r;
  color c;
  
  Circle(float xin, float yin){
    x = xin;
    y = yin;
    c = color(random(255),255,255);
  }
  
  void display(){
    noStroke();
    fill(c);
    ellipse(x,y,2*r,2*r);
  }
  
  void grow(float rmax){
    for(float ri=2; ri<rmax; ri+=1){
      r = ri;
      boolean sign1 = false;
      for(Circle c : circles){
        if(dist(x,y,c.x,c.y) <= c.r+r){
          sign1 = true;
          break;
        }
      }
      if(sign1){
        break;
      }
      boolean sign2 = false;
      for(int i=0; i<360; i++){
        float rad = radians(i);
        float xa = x+cos(rad)*r;
        float ya = y+sin(rad)*r;
        int xs = (int) (xa-shiftx);
        int ys = (int) (ya-shifty);
        if(xs<0 || xs>=img.width || ys<0 || ys>=img.height) break;
          int loc = (int) (xs+ys*img.width);
          float b = brightness(img.pixels[loc]);
          if(b<50){
            sign2 = true;
            break;
          }
        }
      if(sign2){
        break;
      }
    }
  }
}

void mousePressed(){
  save("apple2.png");
}
