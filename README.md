# Python Calculator

One of the go-to projects for programming beginners is a simple calculator.
With these the User is usually tasked with breaking the expression up into its tokens.
This calculator however does it for you.

With a lexical analyzer and a parser which can handle addition, subtraction, multiplication and devision the script will generate an abstract syntax tree from an input string and use a recoursive interpreter to traverse it.

## Usage

To run a calculation type:

```
$ python3 calculator.py <term>
```

or to run the builtin tests run

```
$ python3 calculator.py -t
```

Example:

```
$ python3 calculator.py "2 - ((8 / 4) * ( 3*5-13 ))"
2 - ((8 / 4) * ( 3*5-13 )) = -2.0
```

## Credit

I am currently learning on how to write a simple interpreter by following along [a blog by Ruslan Spivak](https://ruslanspivak.com/lsbasi-part1) for a game I am making.

A large portion of this projects code was **heavily** inspired by his tutorial.
