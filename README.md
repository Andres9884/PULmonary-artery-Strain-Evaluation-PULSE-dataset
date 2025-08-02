# Tool to manipulate files pre and post Ansys simulation
### <p style="font-family:Courier New; font-size:18px;">
This repository presents two different alternatives, using Python, to obtain the same result: the deformed model resulting from a finite element analysis. The first alternative is based on the use of a Python library that takes the ANSYS result file after the simulation and, through internal processing, exports a file in .vtk format, which can be visualized in 3D analysis and visualization applications. The second alternative allows obtaining the same result, but with the advantage of having the exact coordinates of each node of the deformed structure, generating a table with the individual nodes and their coordinates (x, y, z). Thus, while the first alternative produces a three-dimensional file for direct visualization, the second provides detailed access to the information of each node in tabular format.
</p>

## System Requirements
<ul style="font-family:Courier New; font-size:18px;">
  <li>Windows</li>
  <li>Python v3.10.0</li>
  <li>Paraview: for visualising results, can display VTK files and convert a node table into a 3D structure</li>
  <li>Ansys Mechanical APDL: for simulation using input files.</li>
  <li>(OPTIONAL) ICEM CFD: for creating computational models as an input for Ansys Mechanical APDL</li>
</ul>

<p style="font-family:Courier New; font-size:18px;">
  For simulation .in files, resulting from ICEM CFD modeling, were used as an input of Ansys Mechanical APDL, it is possible, for example, to convert .inp files from Abaqus to .in files. Because of that, we recommend to use .in files from ICEM CFD.
</p>

## Previous steps
<ol style="font-family:Courier New; font-size:18px;">
  <li>Clone this repository to a local directory</li>
  <li>In Python, open the terminal and run <code>pip install -r reqs.txt</code></li>
  <li>It is recommended to organize a folder with <code>.in</code> files and create another to keep the outputs</li>
</ol>

## Code usage Alternative 1

<ol style="font-family:Courier New; font-size:18px;">
  <li>In <code>COMMAND.cmd</code>, change the commented lines with the paths you are going to use. Do the same with <code>DATA_CHANGE.py</code> (this file is intended to change files to specific <code>.in</code> parameters, and you can edit it to change these parameters), <code>PyAnsys.py</code>, and <code>get_coords.py</code>.</li>
  <li>Run <code>COMMAND.cmd</code> by executing it as an application.</li>
  <li>Run <code>PyAnsys.py</code>. You will obtain two files per model: one not deformed and one deformed.</li>
  <li>Using <strong>Paraview</strong>, visualize the resulting <code>.vtk</code> files.</li>
</ol>

## Code usage Alternative 2
<p style="font-family:Courier New; font-size:18px;">
  Follow steps 1 and 2. Since <code>get_coords.py</code> file is desigend to process one file at a time, you can simply implement an iterative code to obtain the result of the whole foler (if you have several <code>.in</code> files)
</p>
<ol style="font-family:Courier New; font-size:18px;">
  <li>Run <code>get_coords.py</code>. You will obtain two files per model: one not deformed and one deformed but with <code>csv</code> format.</li>
  <li>Using <strong>Paraview</strong>, visualize the resulting <code>.csv</code> files.</li>
</ol>
