DIR_PYROOT := genC
DIR_BIN := bin
DIR_DBS := dbs

DIR_GEN := $(DIR_PYROOT)/gen
DIR_SRC := $(DIR_PYROOT)/src
DIR_SRC_SQL := $(DIR_SRC)/sql
DIR_BIN_UTILS := $(DIR_BIN)/utils
DIR_UTILS := $(DIR_PYROOT)/utils

DIR_VIRT := $(DIR_PYROOT).virtualenv
BIN_VIRT := $(DIR_VIRT)/bin/activate
PY := $(DIR_VIRT)/bin/python

#DEBUG := 1

PERCENT := %
$(eval DIRS := $(foreach var,$(filter-out %_$(PERCENT)%,$(filter DIR_%,$(shell cat Makefile))),$$($(var))))

C_FILES := $(patsubst %.py2c,$(DIR_GEN)/%.c,$(notdir $(wildcard $(DIR_SRC)/*.py2c)))
SQL_SCHEMAS := $(wildcard $(DIR_SRC_SQL)/*.sql)

BINS := $(patsubst %.c,$(DIR_BIN)/%,$(notdir $(C_FILES)))
BINS_UTILS := $(patsubst %.py,$(DIR_BIN_UTILS)/%,$(notdir $(wildcard $(DIR_SRC)/*.py)))

DBS := $(patsubst %.sql,$(DIR_DBS)/%.sqlite3,$(notdir $(SQL_SCHEMAS)))
PIPELINES := $(patsubst %.pipes,$(DIR_BIN)/%.pipeline,$(notdir $(wildcard $(DIR_SRC)/*.pipes)))

UTILS := $(wildcard $(DIR_UTILS)/*.py)

BOOTSTRAP := $(DIR_BIN_UTILS)/py2bin

all: $(BIN_VIRT) $(C_FILES) $(BOOTSTRAP) $(BIN_UTILS) $(BINS) $(DBS) $(PIPELINES)

$(DIR_GEN)/%.c : $(DIR_SRC)/%.py2c | $(DIR_GEN)
	$(PY) $^ > $@

$(DIR_BIN)/% : $(DIR_GEN)/%.c | $(DIR_BIN)
	gcc $^ -o $@

$(DIR_BIN_UTILS)/py2bin : $(DIR_SRC)/py2bin.py $(UTILS) | $(DIR_BIN_UTILS)
	$(PY) $(filter-out $(UTILS),$^) $(filter-out $(UTILS),$^) $(PY) > $@
	chmod +x $@

$(DIR_BIN_UTILS)/% : $(DIR_SRC)/%.py $(UTILS) | $(DIR_BIN_UTILS)
	$(DIR_BIN_UTILS)/py2bin $(filter-out $(UTILS),$^) $(PY) > $@
	chmod +x $@

$(DIR_DBS)/%.sqlite3 : $(DIR_SRC_SQL)/%.sql | $(DIR_DBS)
	$(PY) $(DIR_UTILS)/db.py init $^ -o $@

$(DIR_BIN)/%.pipeline : $(DIR_SRC)/%.pipes $(DIR_BIN_UTILS)/construct_pipeline
	$(filter $(DIR_BIN)%,$^) -o $@ $(filter %.pipes,$^)
	chmod +x $@
	@[ -z $(DEBUG) ] || cat $@

$(BIN_VIRT): setup.py requirements.txt
	virtualenv $(DIR_VIRT) && source $(BIN_VIRT) && pip install -r requirements.txt

$(DIRS):
	@mkdir -p $@

.PHONY : binutils
