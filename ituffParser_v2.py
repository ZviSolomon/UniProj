import xlsxwriter

ituff = open ("L:\Class\users\SPF\Cross-TP content dependency mapping\Python\ituff.txt", "r");

workbook = xlsxwriter.Workbook('L:\Class\users\SPF\Cross-TP content dependency mapping\Python\ituffTable2.xlsx');

worksheet = workbook.add_worksheet();

worksheet.set_column(0, 8, 30);

bold = workbook.add_format({'bold': 1})

worksheet.write('A1', 'lot', bold); #+0
worksheet.write('B1', 'operation', bold); #+1
worksheet.write('C1', 'visual_id', bold); #+2
worksheet.write('D1', 'tname', bold); #+3
worksheet.write('E1', 'mrslt', bold); #+4
worksheet.write('F1', 'strgval', bold); #+5
worksheet.write('G1', 'psnbinary', bold); #+6
worksheet.write('H1', 'category', bold); #+7
worksheet.write('I1', 'composite', bold); #+8
worksheet.write('J1', 'test_program_name', bold); #+9

row = 1;
col = 0;

while True:
	current_line = ituff.readline();
	if not current_line: break
	splited_line = current_line.split('_'); 
	if (splited_line[1] == 'prgnm'): 
		current_prgnm = splited_line[2];
	elif (splited_line[1] == 'lotid'): 
		current_lot = splited_line[2];
	elif (splited_line[1] == 'lcode'): 
		current_operation = splited_line[2];		
	elif (splited_line[1] == 'visualid'): 
		current_vid = splited_line[2];
	elif (splited_line[1] == 'tname'):
		current_tname = "_".join(splited_line[2:]);
	elif (splited_line[1] == 'mrslt'):
		current_mrslt = splited_line[2];
		worksheet.write_string(row, col, current_lot);
		worksheet.write_string(row, col+1, current_operation);
		worksheet.write_string(row, col+2, current_vid);
		worksheet.write_string(row, col+3, current_tname);
		worksheet.write_string(row, col+4, current_mrslt);
		worksheet.write_string(row, col+9, current_prgnm);
		row += 1;	
	elif (splited_line[1] == 'psnbinary'):
		current_psnbinary = splited_line[2];
		worksheet.write_string(row, col, current_lot);
		worksheet.write_string(row, col+1, current_operation);		
		worksheet.write_string(row, col+2, current_vid);
		worksheet.write_string(row, col+3, current_tname);
		worksheet.write_string(row, col+6, current_psnbinary);
		worksheet.write_string(row, col+9, current_prgnm);
		row +=1;
	elif (splited_line[1] == 'strgval'):
		current_strgval = splited_line[2];
		worksheet.write_string(row, col, current_lot);
		worksheet.write_string(row, col+1, current_operation);		
		worksheet.write_string(row, col+2, current_vid);
		worksheet.write_string(row, col+3, current_tname);
		worksheet.write_string(row, col+5, current_strgval);
		worksheet.write_string(row, col+9, current_prgnm);
		row +=1;
	elif (splited_line[1] == 'category'):
		current_category = splited_line[2];
	elif(splited_line[1] == 'composite'):
		current_composite = "_".join(splited_line[2:]);
		worksheet.write_string(row, col, current_lot);
		worksheet.write_string(row, col+1, current_operation);		
		worksheet.write_string(row, col+2, current_vid);
		worksheet.write_string(row, col+3, current_tname);
		worksheet.write_string(row, col+7, current_category);		
		worksheet.write_string(row, col+8, current_composite);
		worksheet.write_string(row, col+9, current_prgnm);
		row +=1;
		

workbook.close();

