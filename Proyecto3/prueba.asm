.data
num1: .word 3  
num2: .word 9  
resAdd: .word 0  
resSub: .word 0  
resMul: .word 0  
resDiv: .word 0  

.text
main:
    lw $t0, num1   
    lw $t1, num2   

    add $t2, $t0, $t1      
    sw $t2, resAdd

    sub $t3, $t1, $t0      
    sw $t3, resSub

    mul $t4, $t0, $t1      
    sw $t4, resMul

    div $t5, $t1, $t0  
    sw $t5, resDiv 
