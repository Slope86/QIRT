r"""Module to convert various data types to LaTeX representation.

This module provides functions to convert complex numbers, matrices, quantum states,
and measurement results into LaTeX formatted strings. The formatted strings can be
rendered as images using IPython's display capabilities with KaTeX support.

The functionalities added in this module are:

- Conversion of matrices to LaTeX representation.
- Conversion of quantum states to LaTeX ket notation.
- Conversion of measurement results to LaTeX representation.
- Rendering LaTeX code as images using external tools like pdflatex and pdftocairo.

For more information on the LaTeX functions supported by KaTeX, please refer to:
[https://katex.org/docs/supported.html](https://katex.org/docs/supported.html)
"""

from __future__ import annotations

import math
import re
import typing

import numpy as np
import sympy
from IPython.display import Latex

from QIRT.utils import Ket, find_nth_substring, float_gcd

if typing.TYPE_CHECKING:
    from numpy.typing import NDArray

    from QIRT.quantum_state import QuantumState


def matrix_to_latex(
    matrix: NDArray[np.float128 | np.complex128],
    source: bool = False,
) -> str | Latex:
    """Convert a matrix to its LaTeX representation and render it as an image.

    This function converts a given matrix into a LaTeX formatted string and
    then renders this string as an image.

    Args:
        matrix (NDArray[np.float128 | np.complex128]): The matrix to be converted.
        source (bool, optional): Whether to return the LaTeX source code instead of the image. Defaults to False.

    Returns:
        Latex: The rendered image of the LaTeX representation of the matrix, or the LaTeX source code if source is True.
    """
    prefix = R"$\begin{bmatrix}"
    suffix = R"\end{bmatrix}$"

    # If input is a 1d array, convert it to a column matrix
    if len(matrix.shape) == 1:
        matrix = matrix[np.newaxis].T

    # Extract the common factor from the matrix
    gcd = float_gcd(*np.absolute(matrix.flatten()))
    if not (math.isclose(gcd, 1) or math.isclose(gcd, 0)):
        matrix = matrix / gcd
        pretty_gcd = _num_to_latex_ket(gcd)
        prefix = prefix[:1] + pretty_gcd + prefix[1:]

    # Convert the matrix to latex code
    latex_list: list[str] = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # Convert the value to latex code
            pretty_valve = _num_to_latex_ket(matrix[i][j])
            latex_list.append(pretty_valve)
            # Add line up symbol
            if j != matrix.shape[1] - 1:
                latex_list.append("&")
        # Add line break symbol at the end of each row
        latex_list.append(R"\\[6pt]")

    latex_code = prefix + "".join(latex_list) + suffix
    if source:
        return latex_code
    return Latex(latex_code)


def state_to_latex(
    state: QuantumState,
    current_basis: list[str] | str | None = None,
    target_basis: list[str] | str | None = None,
    show_qubit_index: bool = True,
    output_length: int = 2,
    source: bool = False,
) -> str | Latex:
    """Convert a quantum state to its LaTeX representation and render it as an image.

    This function converts a given quantum state into a LaTeX formatted string and
    then renders this string as an image or returns the LaTeX source code.

    Args:
        state (QuantumState): The quantum state to be converted.
        current_basis (List[str] | str | None, optional): The basis of the input state.
            Defaults to None, which sets it to the Z basis.
        target_basis (List[str] | str | None, optional): The target basis for the conversion.
            Defaults to None, which sets it to the current_basis.
        show_qubit_index (bool, optional): Whether to show the qubit indices in the LaTeX output. Defaults to True.
        output_length (int, optional): The number of terms per line in the LaTeX output, defined as 2^output_length.
            Defaults to 2 (i.e., 4 terms per line).
        source (bool, optional): Whether to return the LaTeX source code instead of the image. Defaults to False.

    Returns:
        str | Latex: The rendered image of the LaTeX representation of the quantum state,
        or the LaTeX source code if source is True.
    """
    prefix = R"$\begin{alignedat}{" + f"{2**(output_length+1)+1}" + R"}&\; \;&\;"
    suffix = R"\end{alignedat}$"
    latex_code = _state_to_latex_ket(
        state=state, current_basis=current_basis, target_basis=target_basis, show_qubit_index=show_qubit_index
    )
    latex_code = _latex_line_break(latex_code, output_length)
    latex_code = prefix + latex_code + suffix
    latex_code = latex_code.replace(R"\;&\;-", R"-&\;")
    if source:
        return latex_code
    return Latex(latex_code)


def measure_result_to_latex(
    measure_state_list: list[QuantumState],
    system_state_list: list[QuantumState],
    measure_basis: list[str],
    system_basis: list[str],
    measure_bit: list[int] | str,
    show_qubit_index: bool = True,
    output_length: int = 2,
    source: bool = False,
) -> str | Latex:
    """Convert measurement results to LaTeX representation.

    This function converts the given measurement results into a LaTeX formatted string
    and then renders this string as an image or returns the LaTeX source code.

    Args:
        measure_state_list (List[QuantumState]): The list of measured quantum states.
        system_state_list (List[QuantumState]): The list of system states after measurement.
        measure_basis (List[str]): The basis in which the measurement was performed.
        system_basis (List[str]): The basis of the system state.
        measure_bit (List[int] | str): The bits (qubits) that were measured. Can be a list of indices or
            a string specifying the bits.
        show_qubit_index (bool, optional): Whether to show the qubit indices in the LaTeX output. Defaults to True.
        output_length (int, optional): The number of terms per line in the LaTeX output, defined as 2^output_length.
            Defaults to 2 (i.e., 4 terms per line).
        source (bool, optional): Whether to return the LaTeX source code instead of the image. Defaults to False.

    Returns:
        str | Latex: The rendered image of the LaTeX representation of the measurement results,
        or the LaTeX source code if source is True.
    """
    if isinstance(measure_bit, str):
        measure_bit = [int(i) for i in measure_bit]

    prefix = R"$\begin{alignedat}{" + f"{2**(output_length+1)+1}" + "}"
    suffix = R"\end{alignedat}$"

    latex_list: list[str] = []
    for measure_state, system_state in zip(measure_state_list, system_state_list):
        if measure_state is not None:
            latex_list.append(
                _state_to_latex_ket(
                    state=measure_state,
                    current_basis=measure_basis,
                    target_basis=measure_basis,
                    qubit_index=measure_bit,
                    show_qubit_index=True,
                )[:-1]
            )
            latex_list.append(R":&\; \;&\;")
            tmp_str = _state_to_latex_ket(
                state=system_state,
                current_basis=system_basis,
                target_basis=system_basis,
                hidden_bit=measure_bit,
                show_qubit_index=show_qubit_index,
            )
            latex_list.append(_latex_line_break(tmp_str, output_length))
            latex_list.append(R"\\\\")
    latex_code = prefix + "".join(latex_list) + suffix
    latex_code = latex_code.replace(R"\;&\;-", R"-&\;")
    if source:
        return latex_code
    return Latex(latex_code)


def _state_to_latex_ket(
    state: QuantumState,
    current_basis: list[str] | str | None = None,
    target_basis: list[str] | str | None = None,
    qubit_index: list[int] | None = None,
    hidden_bit: list[int] = [],
    show_qubit_index: bool = False,
) -> str:
    """Convert a quantum state to its LaTeX ket representation.

    This function converts a given quantum state into a LaTeX formatted ket representation,
    optionally showing qubit indices and hiding specified qubits.

    Args:
        state (QuantumState): The quantum state to be converted.
        current_basis (List[str] | str | None, optional): The basis of the input state.
            Defaults to None, which sets it to the Z basis.
        target_basis (List[str] | str | None, optional): The target basis for the conversion.
            Defaults to None, which sets it to basis with minimum entropy.
        qubit_index (List[int] | None, optional): The indices of the qubits to include in the output.
            Defaults to None, which includes all qubits.
        hidden_bit (List[int], optional): The indices of the qubits to hide in the output.
            Defaults to an empty list.
        show_qubit_index (bool, optional): Whether to show the qubit indices in the LaTeX output.
            Defaults to False.

    Returns:
        str: The LaTeX formatted ket representation of the quantum state.
    """
    if current_basis is None:
        current_basis = ["z"] * state.num_of_qubit
    if isinstance(current_basis, str):
        current_basis = list(current_basis)
    if target_basis is None:
        target_basis = ["*"] * state.num_of_qubit
    if isinstance(target_basis, str):
        target_basis = list(target_basis)
    if qubit_index is None:
        qubit_index = list(range(state.num_of_qubit))

    # If the target basis is set to "-", then hide the corresponding qubit
    hidden_bit = hidden_bit.copy()
    for i, basis in enumerate(target_basis):
        if basis == "-":
            hidden_bit.append(qubit_index[i])

    convert_state, convert_basis = state._basis_convert(target_basis, current_basis)
    data = convert_state.data

    if show_qubit_index:
        qubit_index_str = ",".join([str(i) for i in qubit_index if i not in hidden_bit])
    else:
        qubit_index_str = ""

    def ket_name(i):
        ket = bin(i)[2:].zfill(state.num_of_qubit)
        new_ket = ""
        for b, k, i in zip(convert_basis, ket, qubit_index):
            if i in hidden_bit:
                continue
            match b:
                case "z":
                    new_ket += Ket.z1 if int(k) else Ket.z0
                case "x":
                    new_ket += Ket.x1 if int(k) else Ket.x0
                case "y":
                    new_ket += Ket.y1 if int(k) else Ket.y0
        return new_ket

    data = np.around(data, 15)
    nonzero_indices = np.where(data != 0)[0].tolist()
    latex_terms = _coeffs_to_latex_terms(data[nonzero_indices], decimals=15)

    latex_list: list[str] = []
    for idx, ket_idx in enumerate(nonzero_indices):
        if ket_idx is None:
            latex_list.append(R" + \ldots ")
        else:
            term = latex_terms[idx]
            ket = R"\texttt{" + ket_name(ket_idx) + "}"
            latex_list.append(Rf"{term}|{ket}\rangle_{{{qubit_index_str}}} &")

    return "".join(latex_list)


def _coeffs_to_latex_terms(coeffs: NDArray[np.complex128], decimals: int = 15) -> list[str]:
    """Convert a list of coefficients to LaTeX formatted terms.

    The first non-zero term is treated differently by suppressing the leading + sign.

    Args:
        coeffs (NDArray[np.complex128]): List of coefficients to format.
        decimals (int, optional): Number of decimal places to round to. Defaults to 15.

    Returns:
        List[str]: List of LaTeX formatted terms.
    """
    first_term = True
    terms = []
    for coeff in coeffs:
        term = _coeff_to_latex_ket(coeff, first_term, decimals)
        if term is not None:
            first_term = False
        terms.append(term)
    return terms


def _coeff_to_latex_ket(raw_value: complex, first_coeff: bool, decimals: int = 15) -> str | None:
    """Convert a complex coefficient to LaTeX code suitable for a ket expression.

    Args:
        raw_value (complex): The complex value to convert.
        first_coeff (bool): If True, generate LaTeX code for the first term in an expression.
        decimals (int, optional): Number of decimal places to round to. Defaults to 15.

    Returns:
        str | None: LaTeX code representing the coefficient or None if no term is required.
    """
    # Round to the specified number of decimals
    raw_value = np.around(raw_value, decimals=decimals)

    # If the value is zero then return None
    if np.abs(raw_value) == 0:
        return None

    # If the value has both real and imaginary parts, and the real part is negative, then extract the minus sign.
    # for example: +(-0.5+0.5j) -> -(0.5+0.5j)
    real_value = raw_value.real
    imag_value = raw_value.imag
    two_term_sign = "+"
    if np.sign(real_value) == -1 and imag_value != 0:
        two_term_sign = "-"
        raw_value = -raw_value

    # Convert to a sympy expression, then to latex
    value = sympy.nsimplify(raw_value, constants=(sympy.pi,), rational=False)
    latex_element = sympy.latex(value, full_prec=False)

    # Check if the value has more than one term
    two_term = (real_value != 0) and (imag_value != 0)
    if isinstance(value, sympy.Add):
        # can happen for expressions like 1 + sqrt(2)
        two_term = True

    # If the value is 1 or -1 then suppress the coefficient
    if latex_element == "1":
        # If this is the first coefficient then suppress the leading + sign
        if first_coeff:
            return ""
        return "+"
    if latex_element == "-1":
        return "-"

    # If the value has more than one term, wrap it in parentheses
    if two_term:
        # If this is the first coefficient then suppress the leading + sign
        if first_coeff and two_term_sign == "+":
            return f"({latex_element})"
        return f"{two_term_sign}({latex_element})"

    # If this is not the first coefficient and the value is positive then add a leading + sign
    if not first_coeff and latex_element[0] != "-":
        return f"+{latex_element}"

    # Other normal case
    return latex_element


def _num_to_latex_ket(raw_value: complex, decimals: int = 15) -> str:
    """Convert a complex number to a LaTeX element.

    Args:
        raw_value (complex): The complex value to convert.
        decimals (int, optional): Number of decimal places to round to. Defaults to 15.

    Returns:
        str: LaTeX element representing the value.
    """
    raw_value = np.around(raw_value, decimals=decimals)
    value = sympy.nsimplify(raw_value, constants=(sympy.pi,), rational=False)
    return sympy.latex(value, full_prec=False)


def _latex_line_break(latex_code: str, output_length: int = 2) -> str:
    """Split LaTeX string into several lines, so that each line has 2^output_length terms.

    Args:
        latex_code (str): The LaTeX source code to be split into lines.
        output_length (int, optional): The number of terms per line, defined as 2^output_length.
            Defaults to 2 (i.e., 4 terms per line).

    Returns:
        str: The resulting LaTeX code with appropriate line breaks.
    """
    latex_code = latex_code.replace("|", "&|")
    max_term = 2**output_length
    rangle_terms = re.findall(r"\\rangle_\{(?:[0-9](?:,[0-9])*)?\}", latex_code)
    for i in range(max_term, len(rangle_terms), max_term):
        rangle_term = rangle_terms[i - 1]
        new_line_index = find_nth_substring(latex_code, rangle_term, i) + len(rangle_term)
        latex_code = latex_code[:new_line_index] + R"\\ &&" + latex_code[new_line_index + 2 :]

    latex_code = latex_code.replace("&+", R"\;+&\;")
    latex_code = latex_code.replace("&-", R"\;-&\;")
    return latex_code


# import os  # use by function _latex_code_to_img
# import subprocess  # use by function _latex_code_to_img
# import tempfile  # use by function _latex_code_to_img
# from PIL import Image, ImageOps  # use by function _latex_code_to_img
# from qiskit.visualization.exceptions import VisualizationError  # use by function _latex_code_to_img
# from qiskit.visualization.utils import _trim as trim_image  # use by function _latex_code_to_img

# from QIRT.config import get_config_parser  # use by function _latex_code_to_img

# def _latex_code_to_img(latex_code: str) -> Image.Image:
#     """Render LaTeX code to an image.

#     This function converts LaTeX code into an image, using external tools like pdflatex
#     and pdftocairo for the conversion.

#     Args:
#         latex_code (str): The LaTeX code to convert.

#     Returns:
#         PIL.Image.Image: An in-memory representation of the rendered LaTeX code.

#     Raises:
#         MissingOptionalLibraryError: If pillow, pdflatex, or poppler are not installed.
#         VisualizationError: If one of the conversion utilities failed for some internal or file-access reason.
#     """
#     header = R"""
# \documentclass[border=2px]{standalone}

# \usepackage{amsmath}
# \usepackage{graphicx}

# \begin{document}
# """
#     footer = R"\end{document}"
#     latex_source = header + latex_code + footer

#     tmp_filename = "latex_source"
#     with tempfile.TemporaryDirectory() as tmp_dir_name:
#         tmp_path = os.path.join(tmp_dir_name, tmp_filename + ".tex")

#         with open(tmp_path, "w") as tmpfile:
#             tmpfile.write(latex_source)

#         try:
#             subprocess.run(
#                 [
#                     "pdflatex",
#                     "-halt-on-error",
#                     f"-output-directory={tmp_dir_name}",
#                     f"{tmp_filename + '.tex'}",
#                 ],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.DEVNULL,
#                 check=True,
#             )
#         except OSError as exc:
#             # OSError should generally not occur, because it's usually only triggered if `pdflatex`
#             # doesn't exist as a command, but we've already checked that.
#             raise VisualizationError("`pdflatex` command could not be run.") from exc
#         except subprocess.CalledProcessError as exc:
#             with open("latex_error.log", "wb") as error_file:
#                 error_file.write(exc.stdout)
#             raise VisualizationError("`pdflatex` call did not succeed: see `latex_error.log`.") from exc

#         base = os.path.join(tmp_dir_name, tmp_filename)

#         try:
#             subprocess.run(
#                 ["pdftocairo", "-singlefile", "-png", "-q", base + ".pdf", base],
#                 check=True,
#             )
#         except (OSError, subprocess.CalledProcessError) as exc:
#             raise VisualizationError("`pdftocairo` failed to produce an image.") from exc

#         config_parser = get_config_parser()
#         boarder_size = config_parser["latex"].getint("image_border_width_px ", 10)

#         with Image.open(base + ".png") as image:
#             image = ImageOps.expand(trim_image(image), border=boarder_size, fill="white")
#             return image
