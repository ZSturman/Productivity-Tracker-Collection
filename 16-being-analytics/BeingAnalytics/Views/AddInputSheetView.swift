//
//  AddInputSheetView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct AddInputSheetView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var vm: CreateActionStateVM
    @State private var showCalculationSheet = false
    @State var shouldDismiss: Bool = false
    
    @State var tempInput: TempInput = TempInput(inputType: .calculate, order: 10000)
    
    var body: some View {
        NavigationStack {
            VStack {
                List {
                    ForEach(InputTypeOptions.allCases, id: \.rawValue ) { inputTypeOption in
                        Text(inputTypeOption.inputTypeName)
                            .onTapGesture {
                                if inputTypeOption.inputTypeName == "Calculate" {
                                
                                    showCalculationSheet.toggle()
                                } else {
                                    vm.addInput(selectedInput: inputTypeOption)
                                    dismiss()
                                }
                            }
                    }
                }
            }
            .sheet(isPresented: $showCalculationSheet) {
                InputSheetCalculate(vm: vm, showCalculationSheet: $showCalculationSheet, shouldDismissParent: $shouldDismiss, tempCalculate: $tempInput)
            }
            .onChange(of: shouldDismiss) { newValue in
                if newValue {
                    self.dismiss()
                }
            }

            .navigationTitle("Add Input")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
    }
    
}
