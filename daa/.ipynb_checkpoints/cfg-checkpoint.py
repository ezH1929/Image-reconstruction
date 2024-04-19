{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "27aa5e99",
   "metadata": {},
   "outputs": [],
   "source": [
    "import argparse\n",
    "import sys\n",
    "\n",
    "\n",
    "defaults = {\t\n",
    "\t'num_of_points' : 30,\n",
    "\t'visualize'     : False,\n",
    "\t'save'          : False,\n",
    "\t'img_height'    : 200,\n",
    "\t'img_width'     : 200,\n",
    "\t'padding'       : 30\n",
    "}\n",
    "\n",
    "parser = argparse.ArgumentParser()\n",
    "\n",
    "parser.add_argument('--num_of_points', default=defaults['num_of_points'], type=int, help=\"Define the number of points to be generated.\")\n",
    "parser.add_argument('--visualize', action='store_true', default=defaults['visualize'], help=\"If you want to visualize the working of the algorithm\")\n",
    "parser.add_argument('--save', action='store_true', default=defaults['save'], help='If you want to save the end result as an image.')\n",
    "parser.add_argument('--height', default=defaults['img_height'], type=int, help='Define the image height')\n",
    "parser.add_argument('--width', default=defaults['img_width'], type=int, help='Define the image width.')\n",
    "parser.add_argument('--padding', default=defaults['padding'], type=int, \n",
    "\t\t\t\thelp='Define the padding size. Padding is used to make sure the points generated are not too close to the image boundary.')\n",
    "\n",
    "\n",
    "args = parser.parse_args()\n",
    "\n",
    "assert args.num_of_points > 3, \"Number of points must be more than 3 !\"\n",
    "assert args.height >= 20, \"Image height must be at least 20!\"\n",
    "assert args.width >= 20, \"Image width must be at least 20!\"\n",
    "assert args.padding*2 <= args.width or args.padding*2 <= args.height, \"Padding size cannot exceed half of the width nor height of the image!\""
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
