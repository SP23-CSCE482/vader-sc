void bob(int x, int y){
    int a =  find(x);
    int b = find(y);

    if(a == b){
        return;
    }

    if(maxsize[a] == maxsize[b]){
        p[b] = a;
        maxsize[a]++;
    }else if(maxsize[a] > maxsize[b]){
        p[b] = a;

    }else{
        p[a]= b;
    }
}