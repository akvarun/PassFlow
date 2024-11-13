INPUT = test.txt

BASE_NAME = $(basename $(INPUT))

run:
	python3 gatorTicket.py $(INPUT)
	@echo "The output has been written in $(BASE_NAME)_output_file.txt"

clean:
	rm -f *_output_file.txt

