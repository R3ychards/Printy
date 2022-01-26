# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/Rico/Desktop/Alfasolution/DEFINITIVE/printer_rel.py'],
             pathex=[],
             binaries=[],
             datas=[('C:/Users/Rico/Desktop/Alfasolution/DEFINITIVE/config.ini', '.'), ('C:/Users/Rico/Desktop/Alfasolution/DEFINITIVE/Order_Compiled.html', '.'), ('C:/Users/Rico/Desktop/Alfasolution/DEFINITIVE/PaperSettings.ini', '.'), ('C:/Users/Rico/Desktop/Alfasolution/DEFINITIVE/SampleOrder.htm', '.'), ('C:/Users/Rico/Desktop/Alfasolution/DEFINITIVE/Application_Support', 'Application_Support/')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='X64_Printy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='C:\\Users\\Rico\\Desktop\\Alfasolution\\DEFINITIVE\\Application_Support\\icon.ico')
