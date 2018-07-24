:: install VS 2017 community with Windows 10 SDK 10.0.6299 otherwise modify PJON-piper.vcxproj to use a different SDK

set PATH=%PATH%;C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin

msbuild /p:Configuration=Release