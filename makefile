# name of the library
LIBNAME = Analysis

#Necessary to use shell built-in commands
SHELL=bash

# figure out os
UNAME := $(shell uname)
BASEDIR = $(shell pwd)

$(shell mkdir -p lib)
$(shell mkdir -p obj)

USERINCLUDES += -I$(ROOTSYS)/include
USERINCLUDES += -I$(ROOFITSYS)/include
USERINCLUDES += -I$(BOOSTPATH)/include
USERLIBS += -L$(ROOTSYS)/lib -lRooFit -lRooFitCore -lRooStats
USERLIBS += $(shell root-config --glibs) -lTMVA -lMinuit -lFoam -lRooFit -lRooFitCore -lRooStats
CXXFLAGS = -Wall -g #-Wl,-rpath=$(BASEDIR)/lib
LDFLAGS = -shared -W -g

CXX=g++
LD=g++

INCLUDE +=  -I $(BASEDIR)/interface
INCLUDE += $(USERINCLUDES)
CXXFLAGS += $(INCLUDE)

LIBS += $(USERLIBS)

# this is where you  would normaly have the lib, bin and source directories
LIBDIR = $(BASEDIR)/lib
EXEDIR = $(BASEDIR)/bin
MACRODIR = $(BASEDIR)/src
SRCDIR = $(BASEDIR)/src
OBJDIR = $(BASEDIR)/obj
INCDIR = $(BASEDIR)/interface
MAINDIR = $(BASEDIR)/main
DOCDIR= $(BASEDIR)/docs
OBJ_EXT=o
MAIN_EXT=cpp

ROOT_DICT=$(PWD)/obj/RootDict.cxx
ROOT_OBJ=$(subst cxx,$(OBJ_EXT),$(ROOT_DICT))
SRCS=$(wildcard $(BASEDIR)/src/*.cc)
EXES=$(wildcard $(BASEDIR)/main/*.cpp)
HEADERS=$(wildcard $(BASEDIR)/interface/*.h)
OBJS=$(subst $(SRCDIR), $(OBJDIR),$(subst cc,$(OBJ_EXT),$(SRCS)))
BINS=$(subst $(MAINDIR), $(EXEDIR),$(subst .$(MAIN_EXT),,$(EXES)))

all: $(LIBDIR)/lib$(LIBNAME).so

$(LIBDIR)/lib$(LIBNAME).so: $(OBJS) $(ROOT_OBJ)
	@echo Building shared library $@
	@$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

$(OBJDIR)/%.$(OBJ_EXT): $(SRCDIR)/%.cc $(ROOT_DICT)
	@echo Making object $@
	@$(CXX) $(CXXFLAGS) -fPIC -c $< -o $@

$(ROOT_OBJ): $(ROOT_DICT)
	@echo Making object $@
	@$(CXX) $(CXXFLAGS) -fPIC -c $^ -o $@

$(ROOT_DICT): $(HEADERS)
	@echo Making dictionary $@
	@rootcint -f $@ -c -L$(ROOFITSYS)/lib -I$(ROOFITSYS)/include $^

vars:
	@echo "LIBS: " $(LIBS)
	@echo "CXXFLAGS: " $(CXXFLAGS)
	@echo "Header files: " $(HEADERS)
	@echo "Source files: " $(SRCS)
	@echo "Root H files: " $(ROOTHEADERS)
	@echo "Root S files: " $(ROOTCLASSES)
	@echo "Object files: " $(OBJS)
	@echo "Executables:  " $(TARGETS)

clean:
	@echo "Cleaning: "
	@echo "  " $(OBJS)
	@echo "  " $(LIBDIR)/lib$(LIBNAME).so
	@echo "  " $(ROOT_DICT)
	@rm -rf $(OBJS) $(LIBDIR)/lib$(LIBNAME).so $(BINS) $(ROOT_DICT)


