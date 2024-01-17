# RAID-Algorithm

Uniform_distribution.py is the file containing the code distributing uniformly control points over a shape.
Parameters : ncontrol_points : the number of control points the user requires.
             input_image : the image/shape that the user wants to get segmented.
             donnee : can take 2 values : 'image' displays the actual result with the image and its control points ; 'error' shows the evolution of the total error for each point added (sum of white error + black error).

Optimized_distribution.py is the file containing the code performing the RAID method over a shape.
Parameters : ncontrol_points : the number of control points the user requires.
             input_image : the image/shape that the user wants to get segmented.
             donnee : can take 2 values : 'image' displays the actual result with the image and its control points ; 'error' shows the evolution of the total error for each point added (sum of white error + black error).

Comparison.py is the file performing a comparison between the uniform distribution and the RAID method.
Parameters : ncontrol_points : the number of control points the user requires.
             input_image : the image/shape that the user wants to get segmented.
