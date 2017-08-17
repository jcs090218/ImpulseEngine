@echo off
:: ========================================================================
:: $File: build.bat $
:: $Date: 2017-08-14 12:29:31 $
:: $Revision: $
:: $Creator: Jen-Chieh Shen $
:: $Notice: See LICENSE.txt for modification and distribution information
::                    Copyright (c) 2017 by Shen, Jen-Chieh $
:: ========================================================================


python setup.py install

python setup.py py2exe
