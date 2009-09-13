VERSION := 0.9
FILES := common.py data_formats.py epg_runner.py epguide.py output_txt.py \
		 output_xmltv.py parser_cp.py parser_wp.py
DIST_FILES := $(FILES) AUTHORS README COPYING ChangeLog get_listing.sh

dist:
	mkdir epguide_$(VERSION)
	cp $(DIST_FILES) epguide_$(VERSION)
	tar zcvf epguide_$(VERSION).tar.gz epguide_$(VERSION)
	rm -rf epguide_$(VERSION)
	