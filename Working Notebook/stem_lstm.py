import hyperspy.api as hs
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def align_spectrum(s):
	"""
	Takes as an input a hyperspy EELS spectrum (s) and uses a reference spectrum to align it

	Input: 
	  - s: Hyperspy EELS spectrum, either as numpy array or hyperspy 

	Return:
	  - aligned hyperspy signal 
	"""
	s_ref = hs.load('0.4s_ref.dm4')[2]

	# align1D requires same amount of timesteps; find the subsets that maximizes number of samples and make deep copies
	max_timesteps = min(s_ref.data.shape[0],s.data.shape[0])
	s0_align = s_ref.inav[:max_timesteps].deepcopy()
	s1_align = s.inav[:max_timesteps].deepcopy()
	
	# Perform alignment
	s0_align.align1D(start=150, end=400, also_align=[s1_align],show_progressbar = False)

	# Now we have the aligment, find the newly calculated offset (which indicates how much to shift relative to the reference spectrum)
	scale = s1_align.axes_manager[1].scale
	size = s1_align.axes_manager[1].size
	offset = s1_align.axes_manager[1].offset
	
	# Also specify the bounds of the energy channels to keep for model; this enables generic cropping
	crop_start = 435.0
	crop_end = 625.0

	# Calculate the new start and end channel indices
	spec_end = offset + scale * size

	new_start = round((crop_start - offset)/scale)
	new_end = round((spec_end - crop_end)/scale)

	s_new_aligned = s.isig[new_start:-new_end].deepcopy()
	
	# One last crop to account for slight rounding errors
	final_aligned_signal = s_new_aligned.isig[:1900].deepcopy()
	return final_aligned_signal

# Scaling
def scale_spectrum(s, return_scaler = False):
    """
    Takes as an input a hyperspy spectrum or numpy array and returns the scaled version of the data in an array

    Input:
      - s: Hyperspy EELS spectrum, either as numpy array or hyperspy 
      - return_scaler: True returns the scikit-learn scaler, which speeds up future scaling and unscaling

    Return:
      - Scaled signal
      - If return_scaler == True, then the scikit-learn scaler is also returned, enabling faster scaling and unscaling in the future
    """
    # Load reference data for scaling
    s_ref = hs.load('0.4s_ref.dm4')[2]

    # Align s_ref to ensure correct bins are scaled
    s_ref_aligned = align_spectrum(s_ref)

    # If passign unaligned spectrum, be sure to align it
    if s_ref_aligned.data.shape[1] != s.data.shape[1]:
        print('The input spectrum was not aligned; it was aligned as part of the scaling process')
        s = align_spectrum(s)

    # Initiate and fit scaler
    scaler = MinMaxScaler()
    scaler.fit(s_ref_aligned)

    # Transform data 
    s_scaled = scaler.transform(s)
    
    if return_scaler:
        return s_scaled, scaler
    else:
        return s_scaled

def LSTM_format(data, window_back, window_forward):
	"""
	Function to format data into the sequences and target spectra expected by the LSTM

	Input:
	  - data: raw data, as a numpy array
	  - window_back: the number of previous sequences used to make the prediction
	  - window_forward: the number of timeframes in the future that is predicted (0 is the next timestep)

	Return:
	  - X: numpy array of the input spectra sequences
	  - y: numpy array of the target spectrum
	"""

    # Each time step uses last 'window' number of changes to predict the next change
	X = []
	y = []
	for i in range(window_back,len(data) - window_forward):
		X.append(data[i-window_back:i])
		y.append(data[i+window_forward])
	
	# Reshape data to format accepted by LSTM
	X, y = np.array(X), np.array(y)
	
	return X, y

