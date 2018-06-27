/* file : c_algorithm.i */
 
/* name of module to use*/
%module c_algorithm
%{
    /* Every thing in this file is being copied in 
     wrapper file. */
 
    /* variable declaration*/
    int matrix[9][9];
%}
 
/* explicitly list functions and variables to be interfaced */
int matrix[9][9];
void print_sudoku();
int number_unassigned(int *row, int *col);
int is_safe(int n, int r, int c);
int solve_sudoku();
int main();

