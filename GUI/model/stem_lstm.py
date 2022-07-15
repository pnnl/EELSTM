import numpy as np
import hyperspy.api as hs
from sklearn.preprocessing import MinMaxScaler

def autocorrelation_plot(s):

	# Code to determine autocorrelation

	# Plot

	return s


def align_spectra(s):
	"""
    Takes as an input a hyperspy EELS spectrum (s) and uses a reference spectrum to align it
    """
	s_ref = hs.load('model/0.4s_ref.dm4')[2]

	# align1D requires same amount of timesteps; find the subsets that maximizes number of samples and make deep copies
	max_timesteps = min(s_ref.data.shape[0], s.data.shape[0])
	s0_align = s_ref.inav[:max_timesteps].deepcopy()
	s1_align = s.inav[:max_timesteps].deepcopy()

	# Perform alignment
	s0_align.align1D(start=150, end=400, also_align=[s1_align], show_progressbar=False)

	# Now we have the aligment, find the newly calculated offset (which indicates how much to shift relative to the reference spectrum)
	scale = s1_align.axes_manager[1].scale
	size = s1_align.axes_manager[1].size
	offset = s1_align.axes_manager[1].offset

	# Also specify the bounds of the energy channels to keep for model; this enables generic cropping
	crop_start = 435.0
	crop_end = 625.0

	# Calculate the new start and end channel indices
	spec_end = offset + scale * size

	new_start = round((crop_start - offset) / scale)
	new_end = round((spec_end - crop_end) / scale)

	s_new_aligned = s.isig[new_start:-new_end].deepcopy()

	# One last crop to account for slight rounding errors
	final_aligned_signal = s_new_aligned.isig[:1900].deepcopy()
	return final_aligned_signal


def LSTM_format(data, window_back, window_forward):
	"""
	Function to format data into the sequences expected by the LSTM
	data is the raw data
	window_back is the number of previous sequences used to make the prediction
	window_forward is the number of timeframes in the future that is predicted (0 is the next timestep)
	"""

	# Check datatypes

	# Each time step uses last 'window' number of changes to predict the next change
	X = []
	y = []
	for i in range(window_back,len(data) - window_forward):
		X.append(data[i-window_back:i])
		y.append(data[i+window_forward])
	
	# Reshape data to format accepted by LSTM
	X, y = np.array(X), np.array(y)
	
	return X, y

def read_EELS(filename, plot = False):
	"""
	Takes a .dm4 file and returns the EELS spectrum component
	plot option specifies whether or not to plot
	returns the EELS spectrum
	"""
	# Check datatype

	# Check that there are EELS files

	# Load the file into hyperspy signal
	s = hs.load(filename)

	s_eels = s[2]

	if plot:
		s_eels.plot()

	return s_eels


# Scaling
def scale_spectra(s, return_scaler=False):
	"""
    Takes as an input a hyperspy spectrum or numpy array and returns the scaled version of the data in an array
    """
	# Load reference data for scaling
	s_ref = hs.load('model/0.4s_ref.dm4')[2]

	# Align s_ref to ensure correct bins are scaled
	s_ref_aligned = align_spectra(s_ref)

	# If passign unaligned spectrum, be sure to align it
	if s_ref_aligned.data.shape[1] != s.data.shape[1]:
		print('The input spectrum was not aligned; it was aligned as part of the scaling process')
		s = align_spectra(s)

	# Initiate and fit scaler
	scaler = MinMaxScaler()
	scaler.fit(s_ref_aligned)

	# Transform data
	s_scaled = scaler.transform(s)

	if return_scaler:
		return s_scaled, scaler
	else:
		return s_scaled


# Unscaling
def unscale_spectra(s, return_scaler=False):
	"""
    Takes as an input a hyperspy spectrum or numpy array and returns the scaled version of the data in an array
    """
	# Load reference data for scaling
	s_ref = hs.load('model/0.4s_ref.dm4')[2]

	# Align s_ref to ensure correct bins are scaled
	s_ref_aligned = align_spectra(s_ref)

	# If passign unaligned spectrum, be sure to align it
	if s_ref_aligned.data.shape[1] != s.data.shape[1]:
		print('The input spectrum was not aligned; it was aligned as part of the scaling process')
		s = align_spectra(s)

	# Initiate and fit scaler
	scaler = MinMaxScaler()
	scaler.fit(s_ref_aligned)

	# Transform data
	s_unscaled = scaler.inverse_transform(s)

	return s_unscaled


def LSTM_format(data, window_back, window_forward):
	"""

    """
	# Each time step uses last 'window' number of changes to predict the next change
	X = []
	y = []
	for i in range(window_back, len(data) - window_forward):
		X.append(data[i - window_back:i])
		y.append(data[i + window_forward])

	# Reshape data to format accepted by LSTM
	X, y = np.array(X), np.array(y)

	return X, y

