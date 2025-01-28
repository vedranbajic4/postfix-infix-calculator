# Python Expression Converter and Calculator
![DSA Project](https://img.shields.io/badge/Course-DSA-orange)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Code Style](https://img.shields.io/badge/code%20style-PEP8-yellow)

## Description
This is a project for course Algorithms and Data structures. It provides a Python implementation of three functions for working with mathematical expressions:  
- **infix_to_postfix**: Converts an infix expression to postfix notation.  
- **calculate_infix**: Evaluates an infix expression and returns the result.  
- **calculate_postfix**: Evaluates a postfix expression and returns the result.  

## Explanation
**Infix expression**: The expression of the form “a operator b” (a + b) i.e., when an operator is in-between every pair of operands.
**Postfix expression**: The expression of the form “a b operator” (ab+) i.e., When every pair of operands is followed by an operator.

## Features
- Converts infix notation to postfix notation.  
- Evaluate postfix expressions to compute their results. 
- Evaluates infix expression to compute their results. 
- Simple, lightweight, and easy to use.  

## Calculate infix expression algorithm
The calculate_infix algorithm uses two stacks: value_stack and operator_stack, to evaluate an infix expression. For example: `(3 + 5) * (2 - 4)`  Here's a brief explanation of how it works:

### Initialization
First, expression is split into tokens using tokenizer. Then two stacks are created for value and for operators.

### Iteration
For each token in the expression:

- **If it's number**: push it onto `value_stack`

- **If it's an opening parenthesis (`(`)**: push it onto the `operator_stack`

- **If it's an operator (`+`, `-`, `*`, `/`)**:
    - While the top of the `operator_stack` has an operator with equal or higher priority:
        - Pop the operator from `operator_stack` and two values from `value_stack`.
        - Perform the operation and push the result back onto `value_stack`.
    - Push the current operator onto `operator_stack`
    
 - **If it's a closing parenthesis (`)`)**
    - While the top of the `operator_stack` is not `(`:
        - Pop the operator from `operator_stack` and two values from `value_stack`.
        - Perform the operation and push the result back onto `value_stack`.
    - Finally, pop the opening parenthesis `(` from `operator_stack` (but don’t push it back).

### Ending algorithm
- After processing the entire expression, if there are still operators in `operator_stack` repeatedly pop the operator and two values from `value_stack`, evaluate the result, and push it back onto `value_stack`.
- The top value in `value_stack` is the result of the expression that has to be returned


## Calculate postfix expression algorithm
The calculate_postfix algorithm uses only one stacks: value_stack to evaluate a postfix expression. For example: `3 5 + 2 4 - *`. Here's a brief explanation of how it works:

### Initialization
First, expression is split into tokens using tokenizer. Then `value_stack` is created.

### Iteration
For each token in the expression:

- **If token is a number**: push it onto `value_stack`

- **If token is an operator (`+`, `-`, `*`, `/`)**:
    - Pop the top two numbers from `value_stack`.
        - The second popped number becomes the left operand.
        - The first popped number becomes the right operand.
    - Perform the operation (`left_operand` `operator` `right_operand`).
    - Push the result back onto `value_stack`.

### Ending algorithm
After processing all tokens, the remaining value in `value_stack` is the result of the postfix expression.


## Conversion algorithm
### Purpose:
The **infix-to-postfix** conversion algorithm rearranges an infix mathematical expression (A + B * C) into postfix notation (A B C * +). Postfix expressions simplify evaluation by eliminating the need for parentheses and operator priority rules.

### Initialization
 - Create an empty stack `operator_stack` to hold operators and parentheses.
- Create an empty string `postfix` to build the final postfix expression.

### Iteration
For each token in the expression:

- **If token is a number**: Append it directly to `postfix`.

- **If the token is an opening parenthesis (`(`)**: Push it onto `operator_stack`.
- **If the token is a closing parenthesis (`)`)**:
    - Pop operators from `operator_stack` and append them to `postfix` until an opening parenthesis (`(`) is     encountered.
    - Discard the `(`.
- **If the token is an operator (`+`, `-`, `*`, `/`)**:
    - While there is an operator on top of `operator_stack` with greater or equal priority, pop it from the `value_stack` and append it to `postfix`.
    - Push the current operator onto `operator_stack`

### Ending algorithm
If any operators remain in `operator_stack`, pop them and append them to `postfix`

The resulting `postfix` string is the postfix expression.

## Requirements
- Python 3.x

No additional libraries are required.

## Installation
Clone this repository or download the files to your local machine:  

```bash
git clone https://github.com/vedranbajic4/postfix-infix-calculator.git
cd <project-folder>
