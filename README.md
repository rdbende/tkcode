# tkcode
Code block and code editor widget for tkinter with syntax highlighting with Pygments for many languages, plenty of properties, for easier handling, built-in read from or save to file, and many more...


### Install
The installation is very easy via pip

```
pip install tkcode
```
or
```
pip3 install tkcode
```


<details>
<summary>Widget arguments</summary>

Arguments | Description | Type | Default (on X11)
-|-|-|-
`autofocus` | If True the widget will automatically get focus on initialization. | bool | False
`autoseparators` | If this option is True and the `undo` option is set, the separators are automatically added to the undo stack after each insertion or deletion. | bool | True
`bg` or `background` | 	The default background color of the text widget. The option might overwritten by the style configuration file. | str | #ffffff
`bd` or `borderwidth` | The width of the border around the text widget. The option might overwritten by the style configuration file.  | int | 2
`blockcursor` | If True the insertion cursor should be a character-sized rectangle. In the `CodeEditor` widget you can change between block, and line cursor with the `Insert` key. | bool | False
`cursor` | The cursor used inside the widget. See https://www.tcl.tk/man/tcl/TkCmd/cursors.html for a full list of cursors. | str | xterm
`endline` | Specifies an integer line index representing the line of the underlying textual data store that should be just after the last line contained in the widget. This allows a text widget to reflect only a portion of a larger piece of text. If instead of an integer an empty string is given, it will configure the widget to end at the very last line in the textual data store. | int | ""
`exportselection` | Normally, text selected within a text widget is exported to be the selection in the window manager. Set exportselection=0 if you don't want that behavior. | int | 1
`font` | The default font for text inserted into the widget. | tuple | ("monospace", 10)
`fg` or `foreground` | The color used for text (and bitmaps) within the widget. The option might overwritten by the style configuration file. | str | #000000
`height` | The height of the widget in lines (not pixels!), measured according to the current font size. | int | 24
`highlightbackground` | The color of the focus highlight when the text widget does not have focus. The option might overwritten by the style configuration file. | str | #d9d9d9
`highlightcolor` | The color of the focus highlight when the text widget has the focus. The option might overwritten by the style configuration file. | str | #000000
`highlighter` | | str | mariana
`highlightthickness` | The thickness of the focus highlight. Default is 1. Set this option to 0 to suppress display of the focus highlight. The option might overwritten by the style configuration file. | int | 1
`inactiveselectbackground` | Specifies the color to use for the selection when the window does not have the input focus. If empty, then no selection is shown when the window does not have the focus. The option might overwritten by the style configuration file. | str | #c3c3c3
`insertbackground` | The color of the insertion cursor. The option might overwritten by the style configuration file. | str | #000000
`insertborderwidth` | Size of the 3-D border around the insertion cursor. The option might overwritten by the style configuration file. | int | 0
`insertofftime` | The number of milliseconds the insertion cursor is off during its blink cycle. Set this option to zero to turn off blinking. | int | 300
`insertontime` | The number of milliseconds the insertion cursor is on during its blink cycle. | int | 600
`insertwidth` | Width of the insertion cursor (its height is determined by the tallest item in its line). | int | 2
`insertunfocussed` | Specifies how to display the insertion cursor when the widget does not have the focus. Valid values: `none` which means to not display the cursor, `hollow` which means to display a hollow box, or `solid` which means to display a solid box. The option might overwritten by the style configuration file. | str | none
`language` | Syntax highlighting language. Supported languages: `ada`, `c`, `css`, `c#`, `c++,` `dart`, `delphi`, `go`, `haskell`, `html`, `java`, `javascript`, `kotlin`, `lisp`, `lua`, `matlab`, `objective-c`, `perl`, `php`, `python`, `r`, `ruby`, `swift`, `tcl`, `typescript` | str | python
`maxundo` | This option sets the maximum number of operations retained on the undo stack. Set this option to -1 to specify an unlimited number of entries in the undo stack. | int | 0
`padx` | The size of the internal padding added to the left and right of the text area. | int | 1
`pady` | The size of the internal padding added above and below the text area. | int | 1
`relief` | The 3-D appearance of the text widget. | str | sunken
`selectbackground` | The background color to use displaying selected text. The option might overwritten by the style configuration file. | str | #c3c3c3
`selectborderwidth` | The width of the border to use around selected text. The option might overwritten by the style configuration file. | int | 0
`selectforeground` | The foreground color to use displaying selected text. The option might overwritten by the style configuration file. | str | #000000
`setgrid` | Specifies a boolean value that determines whether this widget controls the resizing grid for its top-level window. This option is typically used in text widgets, where the information in the widget has a natural size (the size of a character) and it makes sense for the window's dimensions to be integral numbers of these units. These natural window sizes form a grid. If this option is set to `True` then the widget will communicate with the window manager so that when the user interactively resizes the top-level window that contains the widget, the dimensions of the window will be displayed to the user in grid units and the window size will be constrained to integral numbers of grid units. See https://www.tcl.tk/man/tcl8.5/TkLib/SetGrid.html for more info. | bool | False
`spacing1` | Requests additional space above each text line in the widget, using any of the standard forms for screen distances. If a line wraps, this option only applies to the first line on the display. This option may be overridden with -spacing1 options in tags. | int | 0
`spacing2` | For lines that wrap (so that they cover more than one line on the display) this option specifies additional space to provide between the display lines that represent a single line of text. The value may have any of the standard forms for screen distances. This option may be overridden with -spacing2 options in tags. | int | 0
`spacing3` | Requests additional space below each text line in the widget, using any of the standard forms for screen distances. If a line wraps, this option only applies to the last line on the display. This option may be overridden with -spacing3 options in tags. | int | 0
`startline` | Specifies an integer line index representing the first line of the underlying textual data store that should be contained in the widget. This allows a text widget to reflect only a portion of a larger piece of text. Instead of an integer, the empty string can be provided to this configuration option, which will configure the widget to start at the very first line in the textual data store. | int | ""
! `state` !| Determines whether the textbox is editable or not. Don't use it for CodeBlock. | str | normal (CodeEditor), disabled (CodeBlock)
`tabs` | The size of a tab, note that unlike a plain textwidget, it should not be specified in screen distance, but in characters (`ch`) | str | 4ch
`tabstyle` | Specifies how to interpret the relationship between tab stops on a line and tabs in the text of that line. The value must be tabular or wordprocessor. Note that tabs are interpreted as they are encountered in the text. If the tab style is tabular then the n'th tab character in the line's text will be associated with the n'th tab stop defined for that line. If the tab character's x coordinate falls to the right of the n'th tab stop, then a gap of a single space will be inserted as a fallback. If the tab style is wordprocessor then any tab character being laid out will use (and be defined by) the first tab stop to the right of the preceding characters already laid out on that line. | str | tabular
`takefocus` | Determines whether the window accepts the focus during keyboard traversal (`Tab` or `Shift-Tab`). A value of `False` means that the window should be skipped entirely during keyboard traversal. `True` means that the window should receive the input focus as long as it is viewable (it and all of its ancestors are mapped). An empty string value for the option means that the traversal scripts make the decision about whether or not to focus on the window. | bool / empty string | ""
`undo` | Specifies a boolean that says whether the undo mechanism is active or not. | bool | False
`width` | The width of the widget in characters (not pixels!), measured according to the current font size. | int | 80
! `wrap` !| Specifies how to handle lines in the text that are too long to be displayed in a single line of the text's window. Valid values: `wrap` means that each line of text appears as exactly one line on the screen; extra characters that do not fit on the screen are not displayed. In `char` mode each line of text will be broken up into several screen lines if necessary to keep all the characters visible. In char mode a screen line break may occur after any character; in word mode a line break will only be made at word boundaries. In `CodeEditor` and `CodeBlock` this option is explicitly set to `none`. | str | none
! `xscrollcommand` !| Don't use it for CodeBlock. | callable | ""
! `yscrollcommand` !| Don't use it for CodeBlock. | callable | ""

</details>

![image](https://user-images.githubusercontent.com/77941087/123085590-b1afd800-d422-11eb-9c78-e929e202c53f.png)
![image](https://user-images.githubusercontent.com/77941087/123086076-49adc180-d423-11eb-9132-c17de1b05516.png)