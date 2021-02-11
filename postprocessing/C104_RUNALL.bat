set PYCOM=C:\Python27\ArcGIS10.6\python.exe
set PYTHONBINDIR=..\..\bin
set RERUNCBBDIR=..\..\..\..\rerunCBB\bin

ECHO PROCESSING STEP A

%PYCOM% %PYTHONBINDIR%\a1__NFSEG_res_to_gdb_2.0.py
%PYCOM% %PYTHONBINDIR%\a3__NFSEG_optparams_to_gdb_2.0.py
%PYCOM% %PYTHONBINDIR%\a5__NFSEG_propscal_2.0.py
%PYCOM% %PYTHONBINDIR%\a5b__NFSEG_propscal_PUMPSOFF_2.0.py
%PYCOM% %PYTHONBINDIR%\a6__NFSEG_lst_RIVDRN_flow_2.0.py NO
%PYCOM% %PYTHONBINDIR%\a7__NFSEG_XS_2.0.py

ECHO PROCESSING STEP B

%PYCOM% %PYTHONBINDIR%\b1__SetupReRun_files_2.0.py ..\..\rerunCBB\background\water_budget
cd rerunCBB
cd water_budget_rerun
%RERUNCBBDIR%\mfnwt_jd.exe < mfnwt_nfseg_all_to_cbc.in
%RERUNCBBDIR%\cbb_cfd.nfseg.exe < %RERUNCBBDIR%\cbb_cfd.nfseg.in
%RERUNCBBDIR%\nfseg.springflow.exe
%RERUNCBBDIR%\cbb_table.nfseg.exe < %RERUNCBBDIR%\cbb_table.nfseg.in
start excel NFSEG_2001_WaterBudgetAnalysis.xlsm
start excel NFSEG_2009_WaterBudgetAnalysis.xlsm
cd..
cd..

ECHO PROCESSING STEP C

%PYCOM% %PYTHONBINDIR%\c1__NFSEG_cbb_fc_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\c1a__cbbpropscalcs_2.0.py %CD%

ECHO PROCESSING STEP D

%PYCOM% %PYTHONBINDIR%\d1_IBR_mxds2jpeg_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\d2_HSR_mxds2jpeg_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\d3_BCR_mxds2jpeg_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\d4_OGR_mxds2jpeg_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\d5_CPR_mxds2jpeg_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\d6_CRH_mxds2jpeg_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\d7_CRF_mxds2jpeg_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\d8_CRP_mxds2jpeg_2.0.py %CD%

ECHO PROCESSING STEP E ZONEBUDGET

%PYCOM% %PYTHONBINDIR%\e1__NFSEG_Zonebudget_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\e2__NFSEG_Zonebudget_Figures_2.0.py %CD%
%PYCOM% %PYTHONBINDIR%\e2b__NFSEG_Zonebudget_Figures_full_2.0.py %CD%

