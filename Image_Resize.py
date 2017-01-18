from PIL import Image
import os
import sys
import json

App_Icon = 'AppIcon.appiconset'
Launch_Image = 'LaunchImage.launchimage'
Image_Set = 'imageset'
Contents_File = 'File_Attributes.json'

Max_Image_Size = {}
Max_Image_Size[App_Icon] = (1024,1024)
Max_Image_Size[Launch_Image] = [(1536,2008),(2048,1496)]
Max_Image_Size[Image_Set] = (200,280)

def Create_Folder(Folder_Name):
	try:
		os.makedirs(Folder_Name)
		print 'Folder ', str(Folder_Name),' Created'
	except OSError:
		pass

def Check_File_Exists(File_Name):
	return os.path.isfile(File_Name)

def Json_Read(File_Name):
	try:
		f=open(File_Name,'r')
		Data=json.loads(f.read())
		f.close()
	except Exception as e:
		print 'JSON File Read Error',File_Name
		print e.__class__
		print str(e)
	else:
		return Data
		
def Image_Folder_Types_Choice():
	
	print 'Image Folder Types'
	print 'Press A For AppIcon.appiconset Image Folder'
	print 'Press L For LaunchImage.launchimage Image Folder'
	print 'Press I For imageset Image Folder'
	print 'Press E To Exit'
	
	while True:
		
		try:
			Image_Folder_Type = raw_input("Please Enter The Image Folder Type: ")
			Image_Folder_Type = Image_Folder_Type.upper()
		except Exception as e:
			print 'Input Not Recongnized.'
			print 'Please Try Again'
			continue
	
		if Image_Folder_Type not in ['A','L','I','E']:
			print 'Incorrect Input'
			print 'Please Type One Of The Above Mentioned Option'
			continue
		elif Image_Folder_Type == 'E':
			print 'Exiting The Program'
			sys.exit()
		else:
			break
	
	return Image_Folder_Type
	
def Image_File_Name_Input(Image_Folder_Type):
	
	if Image_Folder_Type == 'L':
		Potrait_Image_File_Name = raw_input("Please Enter The Potrait Image File Name: ")
		Landscape_Image_File_Name = raw_input("Please Enter The Landscape Image File Name: ")
	else:
		Potrait_Image_File_Name = raw_input("Please Enter The Image File Name: ")
		Landscape_Image_File_Name = None
		
	if Check_File_Exists(Potrait_Image_File_Name) == False: 
		print Potrait_Image_File_Name, 'Does Not Exist'
		return None
		
	if Image_Folder_Type == 'L' and Check_File_Exists(Landscape_Image_File_Name) == False:
		print Landscape_Image_File_Name, 'Does Not Exist'
		return None
	
	return (Potrait_Image_File_Name,Landscape_Image_File_Name)
	
def Get_Current_Size(File_Name,Image_Folder_Type,Function_Call_Number=0):
	try:
		with Image.open(File_Name) as Image_File:
			Width, Height = Image_File.size
		
		if Image_Folder_Type == 'L':
			Max_Width, Max_Height = Max_Image_Size[Launch_Image][Function_Call_Number]
		elif Image_Folder_Type == 'A':
			Max_Width, Max_Height = Max_Image_Size[App_Icon]	
		elif Image_Folder_Type == 'I':	
			Max_Width, Max_Height = Max_Image_Size[Image_Set]
		else:
			Max_Width, Max_Height = Max_Image_Size[Image_Set]
		
		if(Width < Max_Width or Height < Max_Height):
			print 'The Dimensions Of The Image Provided Are Less Than Required'
			print 'The Dimension Of The Image Given',Width,'x',Height
			print 'The Minimum Dimension Of The Image Required',Max_Width,'x',Max_Height
			return False
			
	except Exception as e:
		print 'Image File Read Error',File_Name
		print e.__class__
		print str(e)
		return False
	else:
		return True

def Get_Image_Folder_Name(Image_Folder_Type,Image_File_Name):
	
	if Image_Folder_Type == 'A':
		Image_Folder_Name = App_Icon
	elif Image_Folder_Type == 'L':
		Image_Folder_Name = Launch_Image
	elif Image_Folder_Type == 'I':
		Image_File_Name = Image_File_Name.split('.')[0]
		Image_Folder_Name = Image_File_Name + '.' + Image_Set
	else:
		Image_File_Name = Image_File_Name.split('.')[0]
		Image_Folder_Name = Image_File_Name + '.' + Image_Set
		
	return Image_Folder_Name

def Create_Image_Folder(Image_Folder_Type,Image_File_Name):
	Image_Folder_Name = Get_Image_Folder_Name(Image_Folder_Type,Image_File_Name)
	Create_Folder(Image_Folder_Name)
	return Image_Folder_Name

def Image_Resize(Image_File_Name,New_File_Name,Image_Folder_Name,Size):
	try:
		Size = Size.split('x')
		Max_Size = (int(Size[0]),int(Size[1]))
		Image_Object = Image.open(Image_File_Name)
		Out_Image_Object = Image_Object.resize(Max_Size)
		Out_Image_Object.save(os.path.join(Image_Folder_Name,New_File_Name))
	except Exception as e:
		print 'Unable To Resize The Image'
		print e.__class__
		print str(e)
	else:
		return True
			
def main():
	
	if Check_File_Exists(Contents_File):
		Image_Attributes = Json_Read(Contents_File)
		if Image_Attributes is None:
			return
	else:
		print Contents_File, 'Not Present'
		return
		
	Image_Folder_Type = Image_Folder_Types_Choice()
		
	Image_File_Name_Result = Image_File_Name_Input(Image_Folder_Type)
	if Image_File_Name_Result is None:
		print 'Image File Names Do Not Exist'
		print 'Please Restart The Program And Try Again'
		return
		
	Potrait_Image_File_Name = Image_File_Name_Result[0]
	Landscape_Image_File_Name = Image_File_Name_Result[1]
	
	Size_Check = Get_Current_Size(Potrait_Image_File_Name,Image_Folder_Type,Function_Call_Number=0)
	if Size_Check == False:
		return
		
	if Landscape_Image_File_Name is not None:
		Size_Check = False
		Size_Check = Get_Current_Size(Landscape_Image_File_Name,Image_Folder_Type,Function_Call_Number=1)
		if Size_Check == False:
			return
	
	Image_Folder_Name = Create_Image_Folder(Image_Folder_Type,Potrait_Image_File_Name)
	
	if Image_Folder_Type == 'I':
		Image_Attributes = Image_Attributes[Image_Set]
	else:
		Image_Attributes = Image_Attributes[Image_Folder_Name]
				
	for Image_Dict in Image_Attributes:
		try:
			Orientation = Image_Dict.get('Orientation','portrait')
			if Orientation == 'portrait':
				Image_File_Name = Potrait_Image_File_Name
			else:
				Image_File_Name = Landscape_Image_File_Name
			
			New_File_Name = Image_Dict.get('File_Name','Not_Found.png')
			Size = Image_Dict.get('Size','10x10')
			
			if Image_Folder_Type == 'I':
				New_File_Name = Image_File_Name.split('.')[0] + New_File_Name
				
			Image_Resize_Result = Image_Resize(Image_File_Name,New_File_Name,Image_Folder_Name,Size)
			if Image_Resize_Result is None:
				raise Exception()
			
		except Exception as e:
			print 'Exception In Image Dict Loop'
			print Image_Dict
			print e.__class__
			print str(e)
			continue
	else:
		print 'Image Processing Complete'
			
if __name__ == '__main__':
	main()
