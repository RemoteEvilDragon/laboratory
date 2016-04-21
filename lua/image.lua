
img=imgread('1.jpg');
info_size=size(img);
height=info_size(1);
width=info_size(2);
spec_img=zeros(height,width,3);
imshow(img);
figure();
%%%%%%%%%%%%%%x(i,j)
cen_x=width/2;
cen_y=height/2;
radius=150;%%%%%you can change it!!!!!!R!!!!!
radius=min(cen_x,cen_y);
for i=1:height
    for j=1:width
        
        distance=(j-cen_x)*(j-cen_x)+(i-cen_y)*(i-cen_y);
    %%%%% r^2=(j-cen_x)*(j-cen_x)+(i-cen_y)*(i-cen_y)!!!!!
    dis=distance^0.5;       
        spec_img(i,j,:)=img(i,j,:);       
        if(distance<=radius^2)                      
           new_j=floor( dis*(j-cen_x)/radius+cen_x);       
           new_i=floor(  dis*(i-cen_y)/radius+cen_y);       
           spec_img(i,j,:)=img(new_i,new_j,:);       
        end                    
    end
end 
imshow(spec_img/255);
